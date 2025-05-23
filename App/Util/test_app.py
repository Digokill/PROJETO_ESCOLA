# filepath: c:\Users\Administrador\Downloads\Escola\PROJETO_ESCOLA\tests\test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 404  # Ajuste conforme a rota esperada