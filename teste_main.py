from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_raiz():
    response = client.get("/")
    assert response.status_code == 200

def test_criar_usuario():
    response = client.post("/usuarios", json={
        "nome": "Teste",
        "email": "teste@email.com",
        "idade": 25
    })
    assert response.status_code == 200

def test_listar_usuarios():
    response = client.get("/usuarios")
    assert response.status_code == 200