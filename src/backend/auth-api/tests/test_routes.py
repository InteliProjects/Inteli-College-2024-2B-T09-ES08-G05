import pytest 
from fastapi.testclient import TestClient
from app.main import app
from faker import Faker
from httpx import AsyncClient
import asyncio

client = TestClient(app)
faker = Faker()

@pytest.fixture
def create_user():
    def _create_user(role="Inspetor"):
        user_data = {
            "email": faker.email(),
            "password": "Senha_teste",
            "name": faker.name(),
            "role": role
        }
        response = client.post("/user/register", json=user_data)
        assert response.status_code == 201
        return user_data
    return _create_user

@pytest.fixture
def login_user(create_user):
    def _login_user(role="Inspetor"):
        user = create_user(role)
        response = client.post("/user/login", data={
            "username": user["email"],
            "password": user["password"]
        })
        assert response.status_code == 200
        token = response.json()["access_token"]
        return {"user": user, "token": token}
    return _login_user

def test_register_and_login(create_user):
    user = create_user()

    login_response = client.post("/user/login", data={
        "username": user['email'],
        "password": user['password']
        })
    
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

def test_invalid_login():
    response = client.post("/user/login", data={
        "username": faker.email(),
        "password": "Senha Inválida"
    })

    assert response.status_code == 401
    assert "Invalid email or passsword" == response.json()["detail"]

def test_coordinator_acess(login_user):
    user_and_token = login_user(role="Coordenador")
    token = user_and_token["token"]


    response =  client.post(
        "/test/coordenador", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200 

def test_acess_denied(login_user):
    user_and_token_invalid = login_user()
    token =  user_and_token_invalid["token"]
    
    response =  client.post(
        "/test/coordenador", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403

@   pytest.mark.asyncio
async def test_simultaneous_logins(create_user):
    user = create_user()

    num_requests = 20

    async def make_request():
        async with AsyncClient(base_url="http://localhost:8000", timeout=30.0) as client:
            response = await client.post('/user/login', data={
        "username": user['email'],
        "password": user['password']
        })
        return response.status_code, response.json()
    
    tasks = [make_request() for _ in range(num_requests)]
    results = await asyncio.gather(*tasks)

    for status_code, data in results:
        assert status_code == 200
        assert "access_token" in data