import pytest
from unittest.mock import patch, MagicMock
from crudPagamento import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('crudPagamento.bd.create_connection')
def test_add_pagamento_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/pagamentos', json={
        'aluno_id': 1,
        'data': '2023-10-01',
        'valor_pago': 150.50,
        'forma_pagamento': 'Cartão de Crédito'
    })

    assert response.status_code == 201
    assert b'Pagamento registrado com sucesso!' in response.data

@patch('crudPagamento.bd.create_connection')
def test_add_pagamento_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/pagamentos', json={
        'aluno_id': 1,
        'data': '2023-10-01',
        'valor_pago': 150.50,
        'forma_pagamento': 'Cartão de Crédito'
    })

    assert response.status_code == 500
    assert b'Failed to connect to the database' in response.data

@patch('crudPagamento.bd.create_connection')
@patch('crudPagamento.logging')
def test_add_pagamento_success_logging(mock_logging, mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/pagamentos', json={
        'aluno_id': 1,
        'data': '2023-10-01',
        'valor_pago': 150.50,
        'forma_pagamento': 'Cartão de Crédito'
    })

    assert response.status_code == 201
    mock_logging.info.assert_called_with('Pagamento do aluno 1 registrado com sucesso.')

@patch('crudPagamento.bd.create_connection')
@patch('crudPagamento.logging')
def test_add_pagamento_db_failure_logging(mock_logging, mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/pagamentos', json={
        'aluno_id': 1,
        'data': '2023-10-01',
        'valor_pago': 150.50,
        'forma_pagamento': 'Cartão de Crédito'
    })

    assert response.status_code == 500
    mock_logging.error.assert_called_with('Erro ao conectar ao banco de dados ao registrar pagamento.')
