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
        'especialidade': 'Matemática',
        'turma_id': 1
    })

    assert response.status_code == 201
    assert b'Professor adicionado com sucesso!' in response.data

@patch('crudProfessor.bd.create_connection')
def test_add_professor_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/professores', json={
        'nome_completo': 'Maria Silva',
        'especialidade': 'Matemática',
        'turma_id': 1
    })

    assert response.status_code == 500
    assert b'Failed to connect to the database' in response.data
