import requests


class HhAPI:

    def __init__(self):

        self.command = ''
        self.params: dict = {}

    def get_employer_id(self, employer_name: str) -> (bool, str):

        self.command = 'employers/'
        self.params = {'text': employer_name,
                       'only_with_vacancies': True}
        is_ok, result = self.make_request()
        self.params.clear()

        if is_ok:
            vacancies_max_count = 0
            employer_id = ''
            for i in result:
                if i['open_vacancies'] > vacancies_max_count:
                    employer_id = i['id']
            return True, employer_id
        else:
            return False, result

    def get_vacancies(self, employer_id: str) -> (bool, list):

        self.command = 'vacancies/'
        self.params = {'employer_id': employer_id,
                       'page': 0,
                       'per_page': 50,
                       'only_with_salary': True,
                       'order_by': 'salary_desc'}
        is_ok, result = self.make_request()
        self.params.clear()
        return is_ok, result

    def make_request(self) -> (bool, list):

        result = requests.get(f'https://api.hh.ru/{self.command}', params=self.params)
        answer = result.json()

        if result.status_code != 200:
            return False, answer['errors']

        if len(answer['items']) == 0:
            return False, 'Ничего не найдено\n'

        return True, answer['items']
