import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Adiciona o diretório App ao sys.path para que seja possível importar módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crudAluno import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('app.crudCateg.bd.create_connection')
def test_create_category_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/categories', json={
        'category_id': 1,
        'category_name': 'Test Category',
        'description': 'Test Description',
        'picture': None
    })

    assert response.status_code == 201
    assert b'Category created successfully' in response.data

@patch('app.crudCateg.bd.create_connection')
@patch('app.crudCateg.logging')
def test_create_category_success_logging(mock_logging, mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/categories', json={
        'category_id': 1,
        'category_name': 'Test Category',
        'description': 'Test Description',
        'picture': None
    })

    assert response.status_code == 201
    mock_logging.info.assert_called_with('Categoria Test Category criada com sucesso.')

@patch('app.crudCateg.bd.create_connection')
def test_create_category_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/categories', json={
        'category_id': 1,
        'category_name': 'Test Category',
        'description': 'Test Description',
        'picture': None
    })

    assert response.status_code == 500
    assert b'Failed to connect to the database' in response.data

@patch('app.crudCateg.bd.create_connection')
@patch('app.crudCateg.logging')
def test_create_category_db_failure_logging(mock_logging, mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/categories', json={
        'category_id': 1,
        'category_name': 'Test Category',
        'description': 'Test Description',
        'picture': None
    })

    assert response.status_code == 500
    mock_logging.error.assert_called_with('Erro ao conectar ao banco de dados ao criar categoria.')

@patch('app.crudCateg.bd.create_connection')
def test_read_category_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1, 'Test Category', 'Test Description', None)

    response = client.get('/categories/1')

    assert response.status_code == 200
    assert b'Test Category' in response.data

@patch('app.crudCateg.bd.create_connection')
def test_read_category_not_found(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None

    response = client.get('/categories/1')

    assert response.status_code == 404
    assert b'Category not found' in response.data