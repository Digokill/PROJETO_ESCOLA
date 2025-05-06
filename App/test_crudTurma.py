import pytest
from unittest.mock import patch, MagicMock
from crudTurma import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('crudTurma.bd.create_connection')
def test_add_turma_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/turmas', json={
        'nome': 'Turma A',
        'professor_responsavel': 'Prof. João',
        'horario': '08:00 - 12:00'
    })

    assert response.status_code == 201
    assert b'Turma adicionada com sucesso!' in response.data

@patch('crudTurma.bd.create_connection')
def test_add_turma_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/turmas', json={
        'nome': 'Turma A',
        'professor_responsavel': 'Prof. João',
        'horario': '08:00 - 12:00'
    })

    assert response.status_code == 500
    assert b'Failed to connect to the database' in response.data
