import pytest
from unittest.mock import patch, MagicMock
from crudAluno import app

@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    yield client

@patch('crudAluno.bd.create_connection')
def test_add_aluno_success(mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/alunos', json={
        'nome_completo': 'João Silva',
        'data_nascimento': '2010-05-15',
        'turma_id': 1
    })

    assert response.status_code == 201
    assert b'Aluno adicionado com sucesso!' in response.data

@patch('crudAluno.bd.create_connection')
@patch('crudAluno.logging')
def test_add_aluno_success_logging(mock_logging, mock_create_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_create_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    response = client.post('/alunos', json={
        'nome_completo': 'João Silva',
        'data_nascimento': '2010-05-15',
        'turma_id': 1
    })

    assert response.status_code == 201
    mock_logging.info.assert_called_with('Aluno João Silva adicionado com sucesso.')

@patch('crudAluno.bd.create_connection')
def test_add_aluno_db_failure(mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/alunos', json={
        'nome_completo': 'João Silva',
        'data_nascimento': '2010-05-15',
        'turma_id': 1
    })

    assert response.status_code == 500
    assert b'Failed to connect to the database' in response.data

@patch('crudAluno.bd.create_connection')
@patch('crudAluno.logging')
def test_add_aluno_db_failure_logging(mock_logging, mock_create_connection, client):
    mock_create_connection.return_value = None

    response = client.post('/alunos', json={
        'nome_completo': 'João Silva',
        'data_nascimento': '2010-05-15',
        'turma_id': 1
    })

    assert response.status_code == 500
    mock_logging.error.assert_called_with('Erro ao conectar ao banco de dados ao adicionar aluno.')

def test_ler_aluno_success(client):
    with patch('crudAluno.Aluno.query.get') as mock_query:
        mock_query.return_value = MagicMock(
            id=1,
            nome_completo='João Silva',
            data_nascimento='2010-05-15',
            turma_id=1
        )

        response = client.get('/alunos/1')
        assert response.status_code == 200
        assert 'João Silva'.encode('utf-8') in response.data

def test_ler_aluno_not_found(client):
    with patch('crudAluno.Aluno.query.get') as mock_query:
        mock_query.return_value = None

        response = client.get('/alunos/1')
        assert 'Aluno não encontrado'.encode('utf-8') in response.data

def test_atualizar_aluno_success(client):
    with patch('crudAluno.Aluno.query.get') as mock_query:
        aluno_mock = MagicMock()
        mock_query.return_value = aluno_mock

        response = client.put('/alunos/1', json={
            'nome_completo': 'João Silva Atualizado',
            'data_nascimento': '2010-05-15',
            'turma_id': 1
        })

        assert response.status_code == 200
        assert b'Aluno atualizado com sucesso!' in response.data

def test_deletar_aluno_success(client):
    with patch('crudAluno.Aluno.query.get') as mock_query:
        aluno_mock = MagicMock()
        mock_query.return_value = aluno_mock

        response = client.delete('/alunos/1')
        assert response.status_code == 200
        assert b'Aluno deletado com sucesso!' in response.data
