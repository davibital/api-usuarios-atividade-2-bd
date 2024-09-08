import psycopg2
from datetime import datetime


class UserModel:
    def __init__(self, cpf: int, name: str, birth_date: str):
        self.cpf = cpf
        self.name = name
        self.birth_date = birth_date

    @staticmethod
    def from_database(db_user: tuple):
        cpf = db_user[0]
        name = db_user[1]
        birth_date = datetime.strftime(db_user[2], "%d/%m/%Y")
        return UserModel(cpf, name, birth_date)

    def to_database(self):
        return (self.cpf, self.name, self.birth_date)

    @staticmethod
    def from_request(request_user: dict):
        birth_date = datetime.strptime(request_user["birth_date"], "%d/%m/%Y").date()
        return UserModel(
            request_user["cpf"], request_user["name"], birth_date
        )

    def to_response(self):
        return {"cpf": self.cpf, "name": self.name, "birth_date": self.birth_date}


class UserDatabase:
    def __init__(self, db_connection: psycopg2.connect):
        self.db_connection = db_connection

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users (cpf BIGINT PRIMARY KEY, name TEXT, birth_date DATE)"
        )
        cursor.close()
        self.db_connection.commit()

    def insert(self, user: UserModel):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (cpf, name, birth_date) VALUES (%s, %s, %s)",
                user.to_database(),
            )
            cursor.close()
            self.db_connection.commit()
        except psycopg2.errors.UniqueViolation:
            cursor.close()
            self.db_connection.rollback()
            raise ValueError("Já existe um usuário cadastrado com esse CPF")

    def read_by_cpf(self, cpf: int):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE cpf = %s", (cpf,))
        user = cursor.fetchone()
        cursor.close()
        self.db_connection.commit()

        if user is None:
            return None

        return UserModel.from_database(user)

    def read_all(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users")
        db_users = cursor.fetchall()
        cursor.close()
        self.db_connection.commit()

        return [UserModel.from_database(db_user) for db_user in db_users]
