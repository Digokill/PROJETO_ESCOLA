# test_crudAlunos.py

import pytest
from crudAluno import criar_aluno, ler_aluno, atualizar_aluno, deletar_aluno
from unittest.mock import patch

def test_criar_aluno():
    aluno = {"id": 1, "nome": "João", "idade": 20}
    resultado = criar_aluno(aluno)
    assert resultado == True

def test_ler_aluno():
    aluno_id = 1
    resultado = ler_aluno(aluno_id)
    assert resultado == {"id": 1, "nome": "João", "idade": 20}

def test_atualizar_aluno():
    aluno_id = 1
    novos_dados = {"nome": "João Silva", "idade": 21}
    resultado = atualizar_aluno(aluno_id, novos_dados)
    assert resultado == True

def test_deletar_aluno():
    aluno_id = 1
    resultado = deletar_aluno(aluno_id)
    assert resultado == True

@patch('crudAluno.logging')
def test_criar_aluno_logging(mock_logging):
    aluno = {"id": 1, "nome": "João", "idade": 20}
    resultado = criar_aluno(aluno)
    assert resultado == True
    mock_logging.info.assert_called_with('Aluno João criado com sucesso.')

@patch('crudAluno.logging')
def test_ler_aluno_logging(mock_logging):
    aluno_id = 1
    resultado = ler_aluno(aluno_id)
    assert resultado == {"id": 1, "nome": "João", "idade": 20}
    mock_logging.info.assert_called_with('Aluno com ID 1 lido com sucesso.')

@patch('crudAluno.logging')
def test_atualizar_aluno_logging(mock_logging):
    aluno_id = 1
    novos_dados = {"nome": "João Silva", "idade": 21}
    resultado = atualizar_aluno(aluno_id, novos_dados)
    assert resultado == True
    mock_logging.info.assert_called_with('Aluno com ID 1 atualizado com sucesso.')

@patch('crudAluno.logging')
def test_deletar_aluno_logging(mock_logging):
    aluno_id = 1
    resultado = deletar_aluno(aluno_id)
    assert resultado == True
    mock_logging.info.assert_called_with('Aluno com ID 1 deletado com sucesso.')