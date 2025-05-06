import pytest
from unittest.mock import patch, MagicMock
from crudPresenca import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('crudPresenca.bd.create_connection')
def test_add_presenca_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/presencas', json={
        'aluno_id': 1,
        'data': '2023-10-01',
        'presente': True
    })

    assert response.status_code == 201
    assert 'Presença registrada com sucesso!'.encode('utf-8') in response.data

@patch('crudPresenca.bd.create_connection')
def test_add_presenca_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/presencas', json={
        'aluno_id': 1,
        'data': '2023-10-01',
        'presente': True
    })

    assert response.status_code == 500
    assert b'Failed to connect to the database' in response.data
