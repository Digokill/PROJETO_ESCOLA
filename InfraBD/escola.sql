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


CREATE TABLE Professor (
    id_professor SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

CREATE TABLE turma (
    id_turma SERIAL PRIMARY KEY,
    nome_turma VARCHAR(50) NOT NULL,
    id_professor INT REFERENCES Professor(id_professor),
    horario VARCHAR(100) NOT NULL
);

CREATE TABLE alunos (
   id_aluno SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    id_turma INT REFERENCES Turma(id_turma),
    nome_responsavel VARCHAR(255) NOT NULL,
    telefone_responsavel VARCHAR(20) NOT NULL,
    email_responsavel VARCHAR(100) NOT NULL,
    informacoes_adicionais TEXT
)



CREATE TABLE Pagamento (
    id_pagamento SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Aluno(id_aluno),
    data_pagamento DATE NOT NULL,
    valor_pago DECIMAL(10, 2) NOT NULL,
    forma_pagamento VARCHAR(50) NOT NULL,
    referencia VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL
);

CREATE TABLE Presenca (
    id_presenca SERIAL PRIMARY KEY,
    id_aluno INT REFERENCES Aluno(id_aluno),
    data_presenca DATE NOT NULL,
    presente BOOLEAN NOT NULL
);

CREATE TABLE Atividade (
    id_atividade SERIAL PRIMARY KEY,
    descricao TEXT NOT NULL,
    data_realizacao DATE NOT NULL
);

CREATE TABLE Atividade_Aluno (
    id_atividade INT REFERENCES Atividade(id_atividade),
    id_aluno INT REFERENCES Aluno(id_aluno),
    PRIMARY KEY (id_atividade, id_aluno)
);

CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nivel_acesso VARCHAR(20) NOT NULL,
    id_professor INT REFERENCES Professor(id_professor)
);


