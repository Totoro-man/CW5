import psycopg2


class Db:
    def __init__(self, config: dict, new_db_name: str = ''):
        """
        Инициируем соединение с БД
        :param config:
        :param new_db_name:
        """
        self.conn = psycopg2.connect(**config)
        self.new_db_name = new_db_name

    def check_database_exist(self):
        """
        Проверяем существование БД
        :return:
        """
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            query = f"SELECT datname FROM pg_catalog.pg_database WHERE datname = '{self.new_db_name}'"
            cur.execute(query)
            result = bool(cur.rowcount)
        return result

    def create_database(self):
        """
        Создаем БД
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute(f'CREATE DATABASE {self.new_db_name}')

    def stop(self):
        """
        Фиксируем записи в БД
        Закрываем соединение с БД
        :return:
        """
        self.conn.commit()
        self.conn.close()

    def init_database(self):
        """
        Создаем БД если ее нет
        :return:
        """
        if not self.check_database_exist():
            self.create_database()
        self.stop()

    def execute_sql_from_file(self, file_path):
        """
        Выполняем скрипты из файла
        :param file_path:
        :return:
        """
        f = open(file_path, 'r', encoding='utf-8')
        queries = f.read()
        with self.conn.cursor() as cur:
            cur.execute(queries)

    def send_request(self, query: str):
        """
        Отправка готового запроса
        :param query:
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute(query)

    def get_companies_and_vacancies_count(self):
        query = ('SELECT employers.name, COUNT(vacancies.*) '
                 'FROM employers '
                 'JOIN vacancies ON vacancies.employer_id = employers.id '
                 'GROUP BY employers.name')
        with self.conn.cursor() as cur:
            cur.execute(query)
            print(cur.fetchall())

    def get_all_vacancies(self):
        query = ('SELECT e.name, v.name, v.salary_from, v.url '
                 'FROM employers AS e '
                 'JOIN vacancies AS v ON v.employer_id = e.id')
        with self.conn.cursor() as cur:
            cur.execute(query)
            print(cur.fetchall())

    def get_avg_salary(self):
        query = 'SELECT AVG(salary_from) FROM vacancies'
        with self.conn.cursor() as cur:
            cur.execute(query)
            print(cur.fetchall())

    def get_vacancies_with_higher_salary(self):
        query = ('SELECT name, salary_from, url FROM vacancies '
                 'WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies) '
                 'ORDER BY salary_from DESC')
        with self.conn.cursor() as cur:
            cur.execute(query)
            print(cur.fetchall())

    def get_vacancies_with_keywords(self, keywords: list):
        query = (f"SELECT name, salary_from, url FROM vacancies "
                 f"WHERE requirement LIKE '%{keywords[0]}%' "
                 f"OR name LIKE '%{keywords[0]}%' "
                 f"OR responsibility LIKE '%{keywords[0]}%' "
                 f"ORDER BY salary_from DESC")
        with self.conn.cursor() as cur:
            cur.execute(query)
            print(cur.fetchall())
