SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
 
DROP TABLE IF EXISTS alunos;
DROP TABLE IF EXISTS turma;
DROP TABLE IF EXISTS professor;
DROP TABLE IF EXISTS pagamento;
DROP TABLE IF EXISTS presenca;
DROP TABLE IF EXISTS atividade;
DROP TABLE IF EXISTS atividade_aluno;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS disciplina;
DROP TABLE IF EXISTS nota;


CREATE TABLE Professor (
    id_professor SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255),
    email VARCHAR(100),
    telefone VARCHAR(20)
);

CREATE TABLE Disciplina (
    id_disciplina SERIAL PRIMARY KEY,
    nome_disciplina VARCHAR(100),
    codigo VARCHAR(20) UNIQUE,
    carga_horaria INT
);

CREATE TABLE turma (
    id_turma SERIAL PRIMARY KEY,
    nome_turma VARCHAR(50),
    id_professor INT REFERENCES Professor(id_professor),
    horario VARCHAR(100),
    ano_letivo INT,
    id_disciplina INT REFERENCES Disciplina(id_disciplina)
);

CREATE TABLE alunos (
   id_aluno SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255),
    data_nascimento DATE,
    id_turma INT REFERENCES Turma(id_turma),
    nome_responsavel VARCHAR(255),
    telefone_responsavel VARCHAR(20),
    email_responsavel VARCHAR(100),
    informacoes_adicionais TEXT
)

CREATE TABLE Pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Aluno(id_aluno),
    data_pagamento DATE,
    valor_pago DECIMAL(10, 2),
    forma_pagamento VARCHAR(50),
    referencia VARCHAR(100),
    status VARCHAR(20)
);

CREATE TABLE Presenca (
    id_presenca SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Aluno(id_aluno),
    data_presenca DATE,
    presente BOOLEAN
);

CREATE TABLE Atividade (
    id_atividade SERIAL PRIMARY KEY,
    descricao TEXT,
    data_realizacao DATE
);

CREATE TABLE Atividade_Aluno (
    id_atividade INT REFERENCES Atividade(id_atividade),
    id_aluno INT REFERENCES Aluno(id_aluno),
    PRIMARY KEY (id_atividade, id_aluno)
);

CREATE TABLE Nota (
    id_nota SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Alunos(id_aluno),
    id_disciplina INT REFERENCES Disciplina(id_disciplina),
    nota DECIMAL(5, 2),
    data_lancamento DATE
);

CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE,
    senha VARCHAR(255),
    nivel_acesso VARCHAR(20),
    id_professor INT REFERENCES Professor(id_professor)
);


