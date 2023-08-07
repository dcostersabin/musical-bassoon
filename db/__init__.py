import psycopg2
from config import get_config
from utils import Singleton


class DBConnection:
    config = get_config()
    conn = None

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=self.config.POSTGRES_DB,
            user=self.config.POSTGRES_USER,
            password=self.config.POSTGRES_PASSWORD,
            host=self.config.POSTGRES_HOST,
        )


@Singleton
class PostgresConnection:
    def __init__(self):
        self.connection = DBConnection().conn


postgres = PostgresConnection.Instance()
conn = postgres.connection
