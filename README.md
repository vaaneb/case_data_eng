# Case Engenharia de Dados - CRUD de Usuários

API REST para operações CRUD de usuários, construída com FastAPI, SQLAlchemy e SQLite.

## Requisitos

- Python 3.9+
- pip

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/vaaneb/case_data_eng.git
cd case_data_eng
```

### 2. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install .
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
LOG_LEVEL=DEBUG
LOG_SQL_QUERIES=False
DATABASE_URL=sqlite:///./case_data_eng.db
```

### 5. Criar o banco de dados

```bash
alembic upgrade head
```

### 6. Iniciar o servidor

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

A documentação interativa (Swagger UI) pode ser acessada em `http://localhost:8000/docs`.

## Endpoints

| Método   | Rota                    | Descrição                          |
|----------|-------------------------|------------------------------------|
| `POST`   | `/api/v1/users/`        | Cria um novo usuário               |
| `GET`    | `/api/v1/users/`        | Lista todos os usuários            |
| `GET`    | `/api/v1/users/{id}`    | Retorna um usuário pelo ID         |
| `PUT`    | `/api/v1/users/{id}`    | Atualiza um usuário pelo ID        |
| `DELETE` | `/api/v1/users/{id}`    | Remove um usuário pelo ID          |

### Exemplo de corpo para criação (POST)

```json
{
  "first_name": "Vanessa",
  "last_name": "Santos",
  "email": "vanessa@example.com",
  "phone": "11999999999",
  "password": "senha123"
}
```

### Exemplo de corpo para atualização (PUT)

Todos os campos são opcionais:

```json
{
  "first_name": "Vanessa"
}
```

## Docker

```bash
docker compose up --build
```

A API estará disponível em `http://localhost:8000` e o banco de dados será criado automaticamente.

## Testes

```bash
pytest tests/ -v
```

## Estrutura do projeto

```
app/
├── core/                   # Configurações e logging
├── models/                 # Models do SQLAlchemy
├── repositories/           # Camada de acesso a dados
├── routers/                # Endpoints da API
├── schemas/                # Schemas de validação (Pydantic)
├── services/               # Regras de negócio
└── infrastructure/
    ├── database/           # Base, sessão e migrations
    └── security/           # Hashing de senha
tests/
├── conftest.py             # Fixtures de teste
└── test_user_endpoints.py  # Testes do CRUD de usuários
```

## Tecnologias

- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **SQLite** - Banco de dados
- **Alembic** - Migrations
- **Pydantic** - Validação de dados
- **Pytest** - Testes
- **Docker** - Containerização
