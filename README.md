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
- **Pesquisa de criação de relatório do aluno**: 
- **Pesquisa de criação de relatório do aluno**: 
- **Pesquisa de criação de relatório do aluno**: 
- **Pesquisa de criação de relatório do aluno**: 
