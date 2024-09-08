# API de Usuários

## Instruções de execução da API

```bash
# Criar ambiente virtual do Python
python -m venv .venv

# Iniciar ambiente virutal

# No ambiente Linux
source .venv/bin/activate

# No ambiente Windows
.venv\Scripts\activate

# Instalar dependências no ambiente virtual
pip install -r requirements.txt

# Iniciar o servidor de desenvolvimento no modo watch
fastapi dev app/main.py
```

O servidor estará iniciado em `http://localhost:8000`. A documentação do Swagger está presente em `http://localhost:8000/docs`

## Observações

É importante lembrar que o banco de dados utilizado foi o PostgreSQL, portanto é necessário iniciar o servidor e definir as variáveis de ambiente no projeto de acordo com as configurações do banco. As variáveis de ambiente utilizadas foram:

-   `DB_HOST` - host do banco de dados
-   `DB_NAME` - nome do banco de dados a ser conectado
-   `DB_USER` - usuário para autenticação no banco de dados
-   `DB_PASSWORD` - senha para autenticação no banco de dados

Caso não seja informado as variáveis de ambiente no arquivo `.env`, serão utilizados os parâmetros padrões de conexão de um banco de dados postgres normal:

```
DB_HOST="localhost"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_NAME="postgres"
```
