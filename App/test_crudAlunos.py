# test_crudAlunos.py

import pytest
from crudAlunos import criar_aluno, ler_aluno, atualizar_aluno, deletar_aluno

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