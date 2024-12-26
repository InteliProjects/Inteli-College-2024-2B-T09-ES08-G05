from fastapi import FastAPI
import psycopg2
from pydantic import BaseModel
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os
from datetime import datetime
from manager_logger import DatabaseManagerLogger

# Carregar variáveis de ambiente
load_dotenv()

# Chave de criptografia para a URL do banco de dados
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())

fernet = Fernet(ENCRYPTION_KEY)

app = FastAPI()

# Inicializar o logger
db_logger = DatabaseManagerLogger()

# Configuração dos bancos de dados
DATABASES = [
    {
        "name": "primary",
        "url": os.getenv("DATABASE_MAIN"),
    },
    {
        "name": "secondary",
        "url": os.getenv("DATABASE_SECONDARY"),
    }
]

# Variáveis para controle do banco de dados atual e queda do banco primário
current_primary = DATABASES[0]
primary_down = False  

# Modelo de resposta para a URL do banco de dados
class DatabaseResponse(BaseModel):
    database_name: str
    connection_url: str

# Função para verificar a conexão com o banco de dados
def check_connection(database_url, database_name):
    try:
        connection = psycopg2.connect(database_url)
        connection.close()
        db_logger.log_connection_check(database_name, True)
        return True
    except Exception as e:
        db_logger.log_connection_check(database_name, False)
        return False

# Função para formatar valores para inserção no banco de dados
def format_value(value):
    if isinstance(value, datetime):
        return f"'{value.isoformat()}'"
    elif value is None:
        return 'NULL'
    else:
        return f"'{value}'"

# Ordem das tabelas para inserção e exclusão
INSERTION_ORDER = ["users", "projects", "access_projects", "files", "history_availability"]
DELETION_ORDER = ["history_availability", "files", "access_projects", "projects", "users"]

# Função para sincronizar os bancos de dados
def sync_databases(source_url, target_url, source_name, target_name):
    import psycopg2

    backup_data = {}
    modifications_made = False

    try:
        db_logger.log_sync_start(source_name, target_name)

        # Conectar aos bancos de dados
        source_conn = psycopg2.connect(source_url)
        target_conn = psycopg2.connect(target_url)

        source_cursor = source_conn.cursor()
        target_cursor = target_conn.cursor()
        
        # Ajustar o timeout
        target_cursor.execute("SET statement_timeout = 600000;")
        source_cursor.execute("SET statement_timeout = 600000;")

        # Fazer backup dos dados no banco secundário
        for table in INSERTION_ORDER:
            source_cursor.execute(f"SELECT * FROM {table}")
            rows = source_cursor.fetchall()

            if source_cursor.description is None:
                raise RuntimeError(f"No data returned for table {table}.")
            
            columns = [desc[0] for desc in source_cursor.description]
            backup_data[table] = {"columns": columns, "rows": rows}

        # Limpar tabelas no banco secundário
        for table in DELETION_ORDER:
            source_cursor.execute(f"DELETE FROM {table}")
        source_conn.commit() 

        # Comparar os dados entre os DBs
        for table in INSERTION_ORDER:
            source_rows = backup_data[table]["rows"]
            source_set = set(source_rows)

            target_cursor.execute(f"SELECT * FROM {table}")
            target_rows = target_cursor.fetchall()
            target_set = set(target_rows)

            if source_set != target_set:
                modifications_made = True

        # Caso haja modificações, sincroniza os bancos
        if modifications_made:
            print("Modifications detected. Syncing databases...")

            # Limpar tabelas no banco primário em ordem de exclusão
            for table in DELETION_ORDER:
                target_cursor.execute(f"DELETE FROM {table}")
            target_conn.commit()

            # Inserir dados no banco primário em ordem de inserção
            for table in INSERTION_ORDER:
                columns = backup_data[table]["columns"]
                rows = backup_data[table]["rows"]

                for row in rows:
                    column_values = [format_value(value) for value in row]

                    # Para a tabela com chave primária composta
                    if table == "access_projects":
                        conflict_columns = "user_id, project_id"
                        set_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns if col not in ["user_id", "project_id"]])
                    
                    # Para tabelas com chave primária única
                    else:
                        conflict_columns = columns[0]
                        set_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns[1:]])

                    insert_update_query = f"""
                    INSERT INTO {table} ({', '.join(columns)})
                    VALUES ({', '.join(column_values)})
                    ON CONFLICT ({conflict_columns})
                    DO UPDATE SET {set_clause};
                    """
                    target_cursor.execute(insert_update_query)

            target_conn.commit()
            db_logger.log_sync_success(source_name, target_name)

        else:
            db_logger.log_no_changes_detected()

        # Fechar conexões
        source_cursor.close()
        target_cursor.close()
        source_conn.close()
        target_conn.close()

    except Exception as e:
        db_logger.log_sync_failure(source_name, target_name, str(e))
        raise RuntimeError(f"Failed to sync databases: {e}")

# Rota para obter a URL do banco de dados
@app.get("/get_database_url", response_model=DatabaseResponse)
async def get_database_url():
    global current_primary, primary_down

    primary_db = DATABASES[0]
    secondary_db = DATABASES[1]

    if check_connection(primary_db["url"], primary_db["name"]):
        if primary_down:
            db_logger.log_primary_recovery()
            sync_databases(secondary_db["url"], primary_db["url"], secondary_db["name"], primary_db["name"])
            primary_down = False

        current_primary = primary_db
    else:
        db_logger.log_primary_down()
        primary_down = True
        current_primary = secondary_db
        db_logger.log_primary_switch(secondary_db["name"])
        
    encrypted_url = fernet.encrypt(current_primary["url"].encode())
    return DatabaseResponse(database_name=current_primary["name"], connection_url=encrypted_url)

# Rota para forçar o banco de dados primário ficar fora do ar
@app.get("/primary_false", response_model=DatabaseResponse)
async def primary_false():
    global primary_down
    primary_down = True
    db_logger.log_primary_down()
    return DatabaseResponse(database_name="primary", connection_url="down")

# Rota para verificar se o banco secundário assumiu, sem precisar realizar a queda real do banco primário
@app.get("/check_down", response_model=DatabaseResponse)
async def check_down():
    global current_primary, primary_down
    encrypted_url = fernet.encrypt(current_primary["url"].encode())

    if primary_down:
        current_primary = DATABASES[1]  
        db_logger.log_primary_switch(DATABASES[1]["name"])
        return DatabaseResponse(
            database_name=current_primary["name"], 
            connection_url=encrypted_url
        )
    else:
        return DatabaseResponse(
            database_name=current_primary["name"], 
            connection_url=encrypted_url
        )