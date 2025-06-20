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
- **Pesquisa de disciplina**: http://localhost:5000/disciplinas
- **Pesquisa de turma utilizando id do professor**: http://localhost:5000/turmas/professor/4
- **Pesquisa de turma utilizando id da turma**: http://localhost:5000/turmas/2
- **Pesquisa de turma utilizando horario**: http://localhost:5000/turmas//horario/Segunda a Sexta, 07:00-10:30
- **Pesquisa de aluno utilizando nome do aluno**: http://localhost:5000/alunos/nome/João da Silva
- **Pesquisa de aluno utilizando nome do responsavel**: http://localhost:5000/alunos/responsavel/Maria da Silva
- **Pesquisa de aluno utilizando o id do aluno**: http://localhost:5000/alunos/id/3
- **Pesquisa de presenca utilizando id do aluno**: http://localhost:5000/presencas/aluno/1
- **Pesquisa de aluno utilizando data da presenca**: http://localhost:5000/presencas/data/Thu, 30 Jan 2025 00:00:00 GMT
- **Pesquisa de nota utilizando id do aluno**: http://localhost:5000/notas/3
- **Pesquisa de pagamento utilizando status**: http://localhost:5000/pagamentos/status/Pago
- **Pesquisa de pagamento utilizando id do aluno**: http://localhost:5000/pagamentos/aluno/1
- **Pesquisa de criação de relatório do aluno**: http://localhost:5000/alunos/exportar_excel
- **Pesquisa de criação de relatório de presença do aluno**: http://localhost:5000/presencas/exportar_excel
- **Para logiin de Usuario**: http://localhost:5000/usuarios/login 



## Exemplos de Json e ordem para teste

- **Professor**: {
  "nome_completo": "João da Silva",
  "email": "joao.silva@email.com",
  "telefone": "(11) 91234-5678",
  "login": "joaosilva",
  "senha": "senhaSegura123"
}
- **Disciplina**: {
  "nome_disciplina": "Matemática",
  "codigo": "MAT101",
  "carga_horaria": 80
}
- **Turma**: {
  "nome_turma": "1º Ano A",
  "id_professor": 1,
  "horario": "Manhã",
  "ano_letivo": 2025,
  "id_disciplina": 2
}
- **Alunos**: {
  "nome_completo": "Maria Souza",
  "data_nascimento": "2012-03-15",
  "id_turma": 1,
  "informacoes_adicionais": "Alergia a leite",
  "email_responsavel": "responsavel.maria@email.com",
  "telefone_responsavel": "(11) 99999-8888",
  "nome_responsavel": "João Souza"
}
- **Atividade**: {
  "descricao": "Prova de Matemática",
  "data_realizacao": "2025-06-30",
  "nome_turma": "1º Ano A"
}
- **Atividade_Aluno**: {
  "id_atividade": 2,
  "id_aluno": 5
}
- **Notas**: {
  "id_aluno": 3,
  "id_disciplina": 1,
  "nota": 8.5,
  "data_lancamento": "2025-06-20"
} 

- **Presença**: {
  "id_aluno": 3,
  "data_presenca": "2025-06-20",
  "presente": true
}

- **Pagamento**: {
  "id_aluno": 3,
  "data_pagamento": "2025-06-20",
  "valor_pago": 350.00,
  "forma_pagamento": "boleto",
  "referencia": "Mensalidade Junho",
  "status": "pago",
  "vencimento": "2025-06-25"
} 
- **Usuario**: {
  "login": "admin",
  "senha": "minhasenha123",
  "nivel_acesso": "administrador",
  "id_professor": null
}