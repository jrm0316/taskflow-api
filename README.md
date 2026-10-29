# TaskFlow API

O TaskFlow é uma API de gerenciamento de tarefas, desenvolvida em Python com FastAPI.

O sistema permite cadastrar, consultar, atualizar e excluir tarefas, armazenando as informações em um banco de dados PostgreSQL.

## Tecnologias utilizadas

- Python: linguagem de programação.
- FastAPI: desenvolvimento da API REST.
- PostgreSQL: banco de dados relacional.
- SQLAlchemy: comunicação com o banco de dados.
- Alembic: gerenciamento das migrações.
- Pytest: testes automatizados.
- Docker: execução da aplicação em contêiner.
- GitHub Actions: integração contínua (CI).

## Configuração do ambiente

O projeto utiliza PostgreSQL como banco de dados.

A conexão é configurada pela variável de ambiente `DATABASE_URL`, que pode ser definida em um arquivo `.env`.

Exemplo de configuração:

```dotenv
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/taskflow
```

## Instalação do projeto

### Pré-requisitos

- Python 3.14 ou superior
- PostgreSQL
- uv (gerenciador de dependências)
- Git

### Instalar as dependências

Após clonar o repositório e acessar a pasta do projeto, execute:

```powershell
uv sync
```

## Migrações do Banco de dados

Após configurar a variável `DATABASE_URL` e criar o banco PostgreSQL, execute:

```powershell
uv run alembic upgrade head
```

Esse comando aplica as migrações pendentes e atualiza a estrutura do banco de dados.

## Executando a API

Após instalar as dependências, configurar o PostgreSQL e aplicar as migrações, execute:

```powershell
uv run uvicorn main:app --reload
```

A API estará disponível em:

http://localhost:8000

Para acessar a documentação interativa (Swagger UI):

http://localhost:8000/docs