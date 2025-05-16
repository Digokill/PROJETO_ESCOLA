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
    # Mock da conexão e cursor do banco de dados
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Simulação de inserção de presença
    response = client.post('/presencas', json={
        'aluno_id': 1,
        'data_presenca': '2023-10-01',
        'presente': True
    })

    # Verificações
    assert response.status_code == 201
    assert 'Presença registrada com sucesso!'.encode('utf-8') in response.data
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO Presenca (id_aluno, data_presenca, presente) VALUES (%s, %s, %s)",
        (1, '2023-10-01', True)
    )

@patch('crudPresenca.bd.create_connection')
def test_add_presenca_db_failure(mock_create_connection, client):
    # Simulação de falha na conexão com o banco de dados
    mock_create_connection.return_value = None

    response = client.post('/presencas', json={
        'aluno_id': 1,
        'data_presenca': '2023-10-01',
        'presente': True
    })

    # Verificações
    assert response.status_code == 500
    assert b'Failed to connect to the database' in response.data

@patch('crudPresenca.bd.create_connection')
@patch('crudPresenca.logging')
def test_add_presenca_success_logging(mock_logging, mock_create_connection, client):
    # Mock da conexão e cursor do banco de dados
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Simulação de inserção de presença
    response = client.post('/presencas', json={
        'aluno_id': 1,
        'data_presenca': '2023-10-01',
        'presente': True
    })

    # Verificações
    assert response.status_code == 201
    mock_logging.info.assert_called_with('Presença do aluno 1 registrada com sucesso.')

@patch('crudPresenca.bd.create_connection')
@patch('crudPresenca.logging')
def test_add_presenca_db_failure_logging(mock_logging, mock_create_connection, client):
    # Simulação de falha na conexão com o banco de dados
    mock_create_connection.return_value = None

    response = client.post('/presencas', json={
        'aluno_id': 1,
        'data_presenca': '2023-10-01',
        'presente': True
    })

    # Verificações
    assert response.status_code == 500
    mock_logging.error.assert_called_with('Erro ao conectar ao banco de dados ao registrar presença.')
