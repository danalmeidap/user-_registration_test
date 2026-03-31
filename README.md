
# User Management API 

API robusta para gerenciamento de usuários desenvolvida com **FastAPI**, utilizando **SQLAlchemy/SQLModel** para persistência e um pipeline completo de testes e qualidade.


## 🛠 Tecnologias e Ferramentas

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/).
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) / [SQLModel](https://sqlmodel.tiangolo.com/).
* **Banco de Dados:** SQLite (Desenvolvimento) com suporte a migrações via **Alembic**.
* **Qualidade de Código:** **Ruff** (Linter/Formatter) e **Pytest** (Testes Automatizados).
* **Gerenciamento de Dependências:** `pyproject.toml`.


## 🔧 Instalação e Ambiente

Este projeto utiliza o padrão moderno de configuração via `pyproject.toml`.



## Como rodar

Para utilizar basta clonar o repositório e usar o comando abaixo:

1. **Clone o repositório:**
   ```bash
    git clone [https://github.com/seu-usuario/nome-do-projeto.git](https://github.com/seu-usuario/nome-do-projeto.git)
    cd nome-do-projeto

2. **Crie e ative o ambiente virtual:**
   ```bash
      python -m venv .venv
    # Windows:
        .venv\Scripts\activate
    # Linux/Mac:
     source .venv/bin/activate

3. **Instale as deoendências**
   ```bash
     pip install -e .[dev]



## Funcionalidades

- [x] Cadastrar um usuário
- [x] Verificar duplicidade
- [x] Modificar um usuário
- [x] Buscar usuário
- [x] Listar usuários correntes
