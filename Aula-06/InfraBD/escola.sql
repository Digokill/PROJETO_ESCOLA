SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
 
DROP TABLE IF EXISTS alunos;

CREATE TABLE alunos (
  aluno_id character varying(5) NOT NULL,
  nome character varying(40) NOT NULL,
  endereco character varying(60),
  cidade character varying(15),
  estado character varying(15),
  cep character varying(10),
  pais character varying(15),
  telefone character varying(24),
)