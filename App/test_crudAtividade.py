import pytest
from unittest.mock import patch, MagicMock
from crudAtividade import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('crudAtividade.bd.create_connection')
def test_add_atividade_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/atividades', json={
        'descricao': 'Prova de Matemática',
        'data_realizacao': '2023-10-15',
        'turma_id': 1
    })

    assert response.status_code == 201
    assert b'Atividade cadastrada com sucesso!' in response.data

@patch('crudAtividade.bd.create_connection')
def test_add_atividade_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/atividades', json={
        'descricao': 'Prova de Matemática',
        'data_realizacao': '2023-10-15',
        'turma_id': 1
    })

    assert response.status_code == 500
    assert b'Failed to connect to the database' in response.data

@patch('crudAtividade.bd.create_connection')
@patch('crudAtividade.logging')
def test_add_atividade_success_logging(mock_logging, mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/atividades', json={
        'descricao': 'Prova de Matemática',
        'data_realizacao': '2023-10-15',
        'turma_id': 1
    })

    assert response.status_code == 201
    mock_logging.info.assert_called_with('Atividade Prova de Matemática cadastrada com sucesso.')

@patch('crudAtividade.bd.create_connection')
@patch('crudAtividade.logging')
def test_add_atividade_db_failure_logging(mock_logging, mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/atividades', json={
        'descricao': 'Prova de Matemática',
        'data_realizacao': '2023-10-15',
        'turma_id': 1
    })

    assert response.status_code == 500
    mock_logging.error.assert_called_with('Erro ao conectar ao banco de dados ao cadastrar atividade.')
