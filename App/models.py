from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Turma(db.Model):
    __tablename__ = 'turmas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    professor_responsavel = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    professor_id = db.Column(db.Integer, ForeignKey('professores.id'), nullable=False)  # Adicionado ForeignKey
    alunos = relationship('Aluno', back_populates='turma')
    professor = relationship('Professor', back_populates='turmas')  # Adicionado relacionamento

class Aluno(db.Model):
    __tablename__ = 'alunos'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, ForeignKey('turmas.id'), nullable=False)
    turma = relationship('Turma', back_populates='alunos')
    atividades = relationship('AtividadeAluno', back_populates='aluno')  # Adicionado relacionamento

class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    valor_pago = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)

class Presenca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, nullable=False)

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    data_realizacao = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, ForeignKey('turmas.id'), nullable=False)
    alunos = relationship('AtividadeAluno', back_populates='atividade')  # Ajustado relacionamento

class Professor(db.Model):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    turmas = relationship('Turma', back_populates='professor')  # Adicionado relacionamento

class AtividadeAluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, ForeignKey('alunos.id'), nullable=False)
    atividade_id = db.Column(db.Integer, ForeignKey('atividades.id'), nullable=False)
    nota = db.Column(db.Float, nullable=False)
    aluno = db.relationship('Aluno', back_populates='atividades')
    atividade = db.relationship('Atividade', back_populates='alunos')  # Ajustado relacionamento

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)  # 'aluno', 'professor', 'administrador'