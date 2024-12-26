import pytest
from fastapi.testclient import TestClient
from cryptography.fernet import Fernet
from manager import app, fernet, DATABASES, primary_down, check_connection

# Instância do cliente de testes
client = TestClient(app)

# Fixture para configurar as variáveis de ambiente
@pytest.fixture
def setup_environment(monkeypatch):
    monkeypatch.setenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
    monkeypatch.setenv("DATABASE_MAIN", "postgresql://test_main")
    monkeypatch.setenv("DATABASE_SECONDARY", "postgresql://test_secondary")

# Fixture para resetar variáveis globais
@pytest.fixture(autouse=True)
def reset_globals():
    global primary_down
    primary_down = False

# Testa se o banco de dados primário aparece quando está disponível
def test_get_database_url_primary_up(setup_environment):
    response = client.get("/get_database_url")
    assert response.status_code == 200, f"Status esperado: 200, recebido: {response.status_code}"

    data = response.json()
    assert data["database_name"] == "primary", f"Esperado 'primary', recebido: {data['database_name']}"

    decrypted_url = fernet.decrypt(data["connection_url"].encode()).decode()
    assert decrypted_url == DATABASES[0]["url"], f"URL esperada: {DATABASES[0]['url']}, URL decifrada: {decrypted_url}"

# Testa se a rota retorna o banco de dados secundário quando o primário está fora do ar
def test_get_database_url_primary_down(setup_environment, monkeypatch):
    
    def mock_check_connection(url):
        return False if url == DATABASES[0]["url"] else True

    monkeypatch.setattr("manager.check_connection", mock_check_connection)

    response = client.get("/get_database_url")
    assert response.status_code == 200, f"Status esperado: 200, recebido: {response.status_code}"

    data = response.json()
    assert data["database_name"] == "secondary", f"Esperado: 'secondary', recebido: {data['database_name']}"

    decrypted_url = fernet.decrypt(data["connection_url"].encode()).decode()
    assert decrypted_url == DATABASES[1]["url"], f"URL esperada: {DATABASES[1]['url']}, URL recebida: {decrypted_url}"

def test_primary_false_endpoint(setup_environment):
    response = client.get("/primary_false")
    assert response.status_code == 200, f"Status esperado: 200, recebido: {response.status_code}"

    data = response.json()
    assert data["database_name"] == "primary", f"Esperado: 'primary', recebido: {data['database_name']}"
    assert data["connection_url"] == "down", f"Esperado: 'down', recebido: {data['connection_url']}"

# Testa se a rota `/check_down` retorna o banco de dados secundário quando o primário está indisponível
def test_check_down_endpoint_secondary_active(setup_environment, monkeypatch):
    response = client.get("/primary_false")
    assert response.status_code == 200, f"Status esperado: 200, recebido: {response.status_code}"

    response = client.get("/check_down")
    assert response.status_code == 200, f"Status esperado: 200, recebido: {response.status_code}"

    data = response.json()
    assert data["database_name"] == "secondary", f"Esperado: 'secondary', recebido: {data['database_name']}"

