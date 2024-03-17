import psycopg2
from psycopg2 import sql


class Db:
    def __init__(self, config: dict, new_db_name: str = ''):
        self.conn = psycopg2.connect(**config)
        self.new_db_name = new_db_name

    def check_database_exist(self):
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            query = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{self.new_db_name}'"
            cur.execute(query)
            result = bool(cur.rowcount)
        return result

    def create_database(self):
        with self.conn.cursor() as cur:
            cur.execute(f'CREATE DATABASE {self.new_db_name}')

    def stop(self):
        self.conn.commit()
        self.conn.close()

    def init_database(self):
        if not self.check_database_exist():
            self.create_database()
        self.stop()

    def execute_sql_from_file(self, file_path):
        f = open(file_path, 'r', encoding='utf-8')
        queries = f.read()
        with self.conn.cursor() as cur:
            cur.execute(queries)

    def send_request(self, query: str):
        with self.conn.cursor() as cur:
            cur.execute(query)