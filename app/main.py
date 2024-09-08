from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from .database import DatabaseConnection
from .users import UserModel, UserDatabase


app = FastAPI()


user_schema = {
    "Usuário": {
        "type": "object",
        "properties": {
            "cpf": {"type": "integer", "example": 12345678900},
            "name": {"type": "string", "example": "Fulano de Tal"},
            "birth_date": {"type": "string", "example": "00/01/2000"},
        },
        "required": ["cpf", "name", "birth_date"],
    }
}

db_connection = DatabaseConnection().getDatabaseConnection()
user_db = UserDatabase(db_connection)
user_db.create_table()


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Requisição inválida. Certifique-se de que os campos estão corretos e com as chaves e valores com aspas duplas. Exemplo: {'cpf': 12345678901, 'name': 'Fulano', 'birth_date': '01/01/2000' }"
        },
    )


@app.get(
    "/users",
    tags=["Usuários"],
    summary="Retorna todos os usuários",
    responses={
        200: {
            "description": "Lista de usuários",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Usuário"},
                    "example": [
                        {
                            "cpf": 12345678901,
                            "name": "Fulano",
                            "birth_date": "01/01/2000",
                        },
                        {
                            "cpf": 10987654321,
                            "name": "Ciclano",
                            "birth_date": "02/02/2000",
                        },
                    ],
                }
            },
        },
        500: {"description": "Erro interno no servidor"},
    },
)
def get_users():
    """
    Retorna todos os usuários cadastrados no banco de dados, cada um com as seguintes informações:

    - **cpf**: CPF do usuário
    - **name**: Nome do usuário
    - **birth_date**: Data de nascimento do usuário
    """
    return user_db.read_all()


@app.get(
    "/users/{cpf}",
    tags=["Usuários"],
    summary="Retorna um usuário",
    responses={
        200: {
            "description": "Usuário encontrado",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Usuário"},
                    "example": {
                        "cpf": 12345678901,
                        "name": "Fulano",
                        "birth_date": "01/01/2000",
                    },
                }
            },
        },
        404: {"description": "Usuário não encontrado"},
        500: {"description": "Erro interno no servidor"},
    },
)
def get_user_by_cpf(cpf: str):
    """
    Retorna um usuário único do banco de dados, com as seguintes informações:

    - **cpf**: CPF do usuário
    - **name**: Nome do usuário
    - **birth_date**: Data de nascimento do usuário
    """
    result = user_db.read_by_cpf(cpf)
    if result is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return result


@app.post(
    "/users",
    tags=["Usuários"],
    summary="Cria um usuário",
    status_code=201,
    responses={
        201: {
            "description": "Usuário criado com sucesso",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Usuário"},
                    "example": {
                        "cpf": 12345678901,
                        "name": "Fulano",
                        "birth_date": "01/01/2000",
                    },
                },
            },
        },
        400: {"description": "Requisição inválida"},
        422: {
            "description": "Requisição inválida",
        },
        500: {"description": "Erro interno no servidor"},
    },
)
def create_user(user: dict):
    """
    Cria um novo usuário com as seguintes informações:

    - **cpf**: CPF do usuário
    - **name**: Nome do usuário
    - **birth_date**: Data de nascimento do usuário
    """
    try:
        user = UserModel.from_request(user)
        user_db.insert(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=400, detail="Requisição inválida")

    return user_db.read_by_cpf(user.cpf)


openapi_schema = app.openapi()

components = openapi_schema["components"]
components["schemas"].update(user_schema)
paths = openapi_schema["paths"]

paths["/users"]["post"]["requestBody"] = {
    "content": {
        "application/json": {
            "schema": {"$ref": "#/components/schemas/Usuário"},
            "example": {
                "cpf": 12345678901,
                "name": "Fulano de Tal",
                "birth_date": "01/01/2000",
            },
        }
    }
}

app.openapi_schema = openapi_schema
