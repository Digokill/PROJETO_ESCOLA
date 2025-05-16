import pytest
from unittest.mock import patch, MagicMock
from crudUsuario import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('crudUsuario.bd.create_connection')
def test_add_usuario_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/usuarios', json={
        'login': 'admin',
        'senha': '123456',
        'nivel_acesso': 'administrador',
        'id_professor': None
    })

    assert response.status_code == 201
    assert 'Usuário adicionado com sucesso!'.encode('utf-8') in response.data

@patch('crudUsuario.bd.create_connection')
def test_add_usuario_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/usuarios', json={
        'login': 'admin',
        'senha': '123456',
        'nivel_acesso': 'administrador',
        'id_professor': None
    })

    assert response.status_code == 500
    assert b'Failed to connect to the database' in response.data

@patch('crudUsuario.bd.create_connection')
@patch('crudUsuario.logging')
def test_add_usuario_success_logging(mock_logging, mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/usuarios', json={
        'login': 'admin',
        'senha': '123456',
        'nivel_acesso': 'administrador',
        'id_professor': None
    })

    assert response.status_code == 201
    mock_logging.info.assert_called_with('Usuário admin adicionado com sucesso.')

@patch('crudUsuario.bd.create_connection')
@patch('crudUsuario.logging')
def test_add_usuario_db_failure_logging(mock_logging, mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/usuarios', json={
        'login': 'admin',
        'senha': '123456',
        'nivel_acesso': 'administrador',
        'id_professor': None
    })

    assert response.status_code == 500
    mock_logging.error.assert_called_with('Erro ao conectar ao banco de dados ao adicionar usuário.')
