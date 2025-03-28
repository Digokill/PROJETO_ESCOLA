from app import db

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    professor_responsavel = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    alunos = db.relationship('Aluno', backref='turma', lazy=True)

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
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    
class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    turmas = db.relationship('Turma', backref='professor', lazy=True)
    
class AtividadeAluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividade.id'), nullable=False)
    nota = db.Column(db.Float, nullable=False)
    aluno = db.relationship('Aluno', backref='atividades', lazy=True)
    atividade = db.relationship('Atividade', backref='alunos', lazy=True)
    
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False)  # 'aluno', 'professor', 'administrador'