import pytest
from unittest.mock import patch, MagicMock
from crudProfessor import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('crudProfessor.bd.create_connection')
def test_add_professor_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/professores', json={
        'nome_completo': 'Maria Silva',
        'email': 'maria.silva@example.com',
        'telefone': '123456789'
    })

    assert response.status_code == 201
    assert b'Professor adicionado com sucesso!' in response.data

@patch('crudProfessor.bd.create_connection')
def test_add_professor_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/professores', json={
        'nome_completo': 'Maria Silva',
        'email': 'maria.silva@example.com',
        'telefone': '123456789'
    })

    assert response.status_code == 500
    assert b'Failed to connect to the database' in response.data

@patch('crudProfessor.bd.create_connection')
@patch('crudProfessor.logging')
def test_add_professor_success_logging(mock_logging, mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/professores', json={
        'nome_completo': 'Maria Silva',
        'email': 'maria.silva@example.com',
        'telefone': '123456789'
    })

    assert response.status_code == 201
    mock_logging.info.assert_called_with('Professor Maria Silva adicionado com sucesso.')

@patch('crudProfessor.bd.create_connection')
@patch('crudProfessor.logging')
def test_add_professor_db_failure_logging(mock_logging, mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/professores', json={
        'nome_completo': 'Maria Silva',
        'email': 'maria.silva@example.com',
        'telefone': '123456789'
    })

    assert response.status_code == 500
    mock_logging.error.assert_called_with('Erro ao conectar ao banco de dados ao adicionar professor.')
