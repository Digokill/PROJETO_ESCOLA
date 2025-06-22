# Projeto Escola - Monitoramento e Logs

Este projeto utiliza Prometheus, Grafana e Postgres Exporter para monitoramento, além de um sistema de logs para análise.

## Passo a Passo

### 1. Subir os serviços com Docker Compose
Certifique-se de que o Docker e o Docker Compose estão instalados. Para iniciar os serviços, execute:

```bash
docker compose up -d --build
```

### 2. Acessar o Prometheus
- URL: [http://localhost:9090](http://localhost:9090)
- O Prometheus coleta métricas do Postgres Exporter e está configurado para monitorar o banco de dados.

#### Verificar status:
1. Acesse a aba **Status > Targets** no Prometheus.
2. Certifique-se de que o endpoint do Postgres Exporter está listado como `UP`.

### 3. Acessar o Grafana
- URL: [http://localhost:3000](http://localhost:3000)
- Credenciais padrão:
  - Usuário: `admin`
  - Senha: `admin`

#### Configurar o Grafana:
1. Faça login no Grafana.
2. Adicione o Prometheus como fonte de dados:
   - Vá para **Configuration > Data Sources**.
   - Clique em **Add data source**.
   - Escolha **Prometheus**.
   - Configure a URL como `http://prometheus:9090` e salve.
3. Importe dashboards:
   - Vá para **Dashboards > Import**.
   - Use um ID de dashboard público ou importe um arquivo JSON.

### 4. Testar Logs
Se o sistema de logs estiver configurado, siga os passos abaixo:

1. Gere logs no sistema:
   - Execute ações no sistema Flask para gerar logs.
2. Verifique os logs:
   - Acesse os arquivos de log no diretório configurado no container ou use ferramentas externas para análise.

### 5. Parar os serviços
Para parar e remover os containers, execute:

```bash
docker compose down
```

## Estrutura do Projeto
- **Prometheus**: Coleta métricas do Postgres Exporter.
- **Grafana**: Visualiza métricas e cria dashboards.
- **Postgres Exporter**: Exporta métricas do banco de dados PostgreSQL.

## Problemas Comuns
- **Erro de conexão no Grafana**: Verifique se o Prometheus está acessível em `http://prometheus:9090`.
- **Serviços não iniciam**: Certifique-se de que o Docker Desktop está em execução.

## Contribuição
Sinta-se à vontade para contribuir com melhorias no projeto. Envie um pull request ou abra uma issue.

## Rotas de Pesquisa
- **Pesquisa de professor utilizando id**: http://localhost:5000/professores/4
- **Pesquisa de disciplina**: http://localhost:5000/disciplinas/2
- **Pesquisa de turma utilizando id do professor**: http://localhost:5000/turmas/professor/2
- **Pesquisa de turma utilizando id da turma**: http://localhost:5000/turmas/3
- **Pesquisa de turma utilizando horario**: http://localhost:5000/turmas/horario/Manhã
- **Pesquisa de aluno utilizando nome do aluno**: http://localhost:5000/alunos/nome/Maria Souza
- **Pesquisa de aluno utilizando nome do responsavel**: http://localhost:5000/alunos/responsavel/João Souza
- **Pesquisa de aluno utilizando o id do aluno**: http://localhost:5000/alunos/id/2
- **Pesquisa de presenca utilizando id do aluno**: http://localhost:5000/presencas/aluno/2
- **Pesquisa de aluno utilizando data da presenca**: http://localhost:5000/presencas/data/Fri, 20 Jun 2025 00:00:00 GMT
- **Pesquisa de nota utilizando id do aluno**: http://localhost:5000/notas/2
- **Pesquisa de pagamento utilizando status**: http://localhost:5000/pagamentos/status/pago
- **Pesquisa de pagamento utilizando id do aluno**: http://localhost:5000/pagamentos/aluno/2
- **Pesquisa de criação de relatório do aluno**: http://localhost:5000/alunos/exportar_excel
- **Pesquisa de criação de relatório de presença do aluno**: http://localhost:5000/presencas/exportar_excel
- **Para login de Usuario**: http://localhost:5000/usuarios/login 



## Exemplos de Json e ordem para teste

- **professor**: {
  "nome_completo": "João da Silva",
  "email": "joao.silva@email.com",
  "telefone": "(11) 91234-5678",
  "login": "joaosilva",
  "senha": "senhaSegura123"
}
- **disciplina**: {
  "nome_disciplina": "Matemática",
  "codigo": "MAT101",
  "carga_horaria": 80
}
- **turma**: {
  "nome_turma": "1º Ano A",
  "id_professor": 1,
  "horario": "Manhã",
  "ano_letivo": 2025,
  "id_disciplina": 2
}
- **alunos**: {
  "nome_completo": "Maria Souza",
  "data_nascimento": "2012-03-15",
  "id_turma": 1,
  "informacoes_adicionais": "Alergia a leite",
  "email_responsavel": "responsavel.maria@email.com",
  "telefone_responsavel": "(11) 99999-8888",
  "nome_responsavel": "João Souza"
}
- **atividades**: {
  "descricao": "Prova de Matemática",
  "data_realizacao": "2025-06-30",
  "nome_turma": "1º Ano A"
}
- **atividades_alunos**: {
  "id_atividade": 1,
  "id_aluno": 2
}
- **notas**: {
  "id_aluno": 2,
  "id_disciplina": 1,
  "nota": 8.5,
  "data_lancamento": "2025-06-20"
} 

- **presencas**: {
  "id_aluno": 2,
  "data_presenca": "2025-06-20",
  "presente": true
}

- **pagamentos**: {
  "id_aluno": 2,
  "data_pagamento": "2025-06-20",
  "valor_pago": 350.00,
  "forma_pagamento": "boleto",
  "referencia": "Mensalidade Junho",
  "status": "pago",
  "vencimento": "2025-06-25"
} 
- **usuarios**: {
  "login": "admin",
  "senha": "minhasenha123",
  "nivel_acesso": "administrador",
  "id_professor": null
}

--------------------------------------------------------



- **professor**: {
  "nome_completo": "Faith Ribeiro",
  "email": "Fé@gmail.com",
  "telefone": "(21) 98888-7777",
  "login": "fe",
  "senha": "Forte456"
}

- **disciplina**: {
  "nome_disciplina": "Geografia",
  "codigo": "GEO201",
  "carga_horaria": 45
}

- **turma**: {
  "nome_turma": "3º Ano C",
  "id_professor": 2,
  "horario": "Noite",
  "ano_letivo": 2025,
  "id_disciplina": 3
}

- **alunos**: {
  "nome_completo": "Xico Com Chis",
  "data_nascimento": "2011-08-22",
  "id_turma": 2,
  "informacoes_adicionais": "Usa Binóculos",
  "email_responsavel": "responsavel.Tuco@email.com",
  "telefone_responsavel": "(21) 97777-6666",
  "nome_responsavel": "Tico Lima"
}

- **atividades**: {
  "descricao": "Trabalho de Geografia Com Terra-Neo",
  "data_realizacao": "2025-07-10",
  "nome_turma": "3º Ano B"
}

- **atividades_alunos**: {
  "id_atividade": 3,
  "id_aluno": 3
}

- **notas**: {
  "id_aluno": 3,
  "id_disciplina": 3,
  "nota": 9.2,
  "data_lancamento": "2025-08-15"
}

- **presencas**: {
  "id_aluno": 3,
  "data_presenca": "2025-08-15",
  "presente": false
}

- **pagamentos**: {
  "id_aluno": 3,
  "data_pagamento": "2025-08-05",
  "valor_pago": 400.00,
  "forma_pagamento": "cartao",
  "referencia": "Mensalidade Agosto",
  "status": "pendente",
  "vencimento": "2025-08-10"
}

- **usuarios**: {
  "login": "secretaria2",
  "senha": "acesso2Secretaria2025",
  "nivel_acesso": "secretaria",
  "id_professor": null
}

- **Pesquisa de criação de relatório do aluno**: http://localhost:5000/alunos/exportar_excel
- **Pesquisa de criação de relatório de presença do aluno**: http://localhost:5000/presencas/exportar_excel
- **Pesquisa de criação de relatório de pagamentos do aluno**: http://localhost:5000/pagamentos/exportar_excel
- **Para login de Usuario**: http://localhost:5000/usuarios/login 
{
  "login": "admin",
  "senha": "minhasenha123"
}








------------------------------------

- **professor**: {
  "nome_completo": "Ana Paula Ribeiro",
  "email": "ana.ribeiro@email.com",
  "telefone": "(21) 98888-7777",
  "login": "anaribeiro",
  "senha": "senhaForte456"
}

- **disciplina**: {
  "nome_disciplina": "História",
  "codigo": "HIS201",
  "carga_horaria": 60
}

- **turma**: {
  "nome_turma": "2º Ano B",
  "id_professor": 2,
  "horario": "Tarde",
  "ano_letivo": 2025,
  "id_disciplina": 3
}

- **alunos**: {
  "nome_completo": "Carlos Eduardo Lima",
  "data_nascimento": "2011-08-22",
  "id_turma": 2,
  "informacoes_adicionais": "Usa óculos",
  "email_responsavel": "responsavel.carlos@email.com",
  "telefone_responsavel": "(21) 97777-6666",
  "nome_responsavel": "Fernanda Lima"
}

- **atividades**: {
  "descricao": "Trabalho de História Antiga",
  "data_realizacao": "2025-07-10",
  "nome_turma": "2º Ano B"
}

- **atividades_alunos**: {
  "id_atividade": 2,
  "id_aluno": 3
}

- **notas**: {
  "id_aluno": 3,
  "id_disciplina": 3,
  "nota": 9.2,
  "data_lancamento": "2025-07-15"
}

- **presencas**: {
  "id_aluno": 3,
  "data_presenca": "2025-07-15",
  "presente": false
}

- **pagamentos**: {
  "id_aluno": 3,
  "data_pagamento": "2025-07-05",
  "valor_pago": 400.00,
  "forma_pagamento": "cartao",
  "referencia": "Mensalidade Julho",
  "status": "pendente",
  "vencimento": "2025-07-10"
}

- **usuarios**: {
  "login": "secretaria",
  "senha": "acessoSecretaria2025",
  "nivel_acesso": "secretaria",
  "id_professor": null
}