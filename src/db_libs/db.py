import psycopg2
from psycopg2 import sql


class Db:
    def __init__(self, password: str, database_name: str):
        self.conn = psycopg2.connect(
                    database="postgres",
                    user='postgres',
                    password=password,
                    host='localhost',
                    port='5432')
        self.conn.autocommit = True
        self.database_name = database_name

    def check_database_exist(self):
        with self.conn.cursor() as cur:
            query = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{self.database_name}'"
            cur.execute(query)
            result = bool(cur.rowcount)
        return result

    def create_database(self):
        with self.conn.cursor() as cur:
            cur.execute(sql.SQL('CREATE DATABASE {};').format(sql.Identifier(self.database_name)))

    def stop(self):
        self.conn.close()

    def init_base(self):
        if not self.check_database_exist():
            self.create_database()
        self.stop()

    def execute_sql_from_file(self, file_path: str):
        f = open(file_path, 'r', encoding='utf-8')
        queries = f.read()
        with self.conn.cursor() as cur:
            cur.execute(queries)