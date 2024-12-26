from logger import Logger

class DatabaseManagerLogger(Logger):
    def __init__(self):
        super().__init__(log_filename='database_manager.log')

    def log_connection_check(self, database_name, status):
        # Log para informar o status da conexão com o banco de dados
        message = f"Database '{database_name}' status de conexão: {'UP' if status else 'DOWN'}"
        self._logger.info("CONNECTION_CHECK", message)

    def log_sync_start(self, source_db, target_db):
        # Log para informar o início da sincronização do banco de dados
        message = f"Começando a sincronização do '{source_db}' para '{target_db}'"
        self._logger.info("SYNC_START", message)

    def log_sync_success(self, source_db, target_db):
        # Log para informar que a sincronização do banco de dados foi bem sucedida
        message = f"'{source_db}' sincronizado com sucesso para '{target_db}'"
        self._logger.info("SYNC_SUCCESS", message)

    def log_sync_failure(self, source_db, target_db, error_message):
        # Log para informar que a sincronização do banco de dados falhou
        message = f" '{source_db}' falhou ao sincronizar para '{target_db}' - {error_message}"
        self._logger.error("SYNC_FAILURE", message)

    def log_primary_switch(self, new_primary_db):
        # Log para informar que o banco de dados primário foi alterado
        message = f"Banco atual alterado para '{new_primary_db}'"
        self._logger.info("PRIMARY_SWITCH", message)

    def log_primary_down(self):
        # Log para informar que o banco de dados primário está fora do ar
        message = "Banco de dados primário está fora do ar"
        self._logger.info("PRIMARY_DOWN", message)

    def log_primary_recovery(self):
        # Log para informar que o banco de dados primário foi recuperado
        message = "Banco de dados primário recuperado"
        self._logger.info("PRIMARY_RECOVERY", message)

    def log_no_changes_detected(self):
        # Log para informar que nenhuma modificação foi detectada entre os bancos de dados
        message = "Nenhuma modificação detectada. Nenhuma ação tomada."
        self._logger.info("NO_CHANGES", message)
