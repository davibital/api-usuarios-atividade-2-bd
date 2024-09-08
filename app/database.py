import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE = os.getenv("DB_NAME", default="postgres")
USER = os.getenv("DB_USER", default="postgres")
PASSWORD = os.getenv("DB_PASSWORD", default="postgres")
HOST = os.getenv("DB_HOST", default="localhost")


class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def getDatabaseConnection(self) -> psycopg2.connect:
        if self.connection is not None:
            return self.connection

        self.connection = psycopg2.connect(
            database=DATABASE, user=USER, password=PASSWORD, host=HOST
        )
        return self.connection
