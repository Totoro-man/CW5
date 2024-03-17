import requests


class HhAPI:

    def __init__(self):

        self.command = ''
        self.params: dict = {}

    def get_employer_profile_url(self, employer_name: str) -> (bool, str):
        """
        Получаем с ХХ ссылку на профиль искомого работодателя
        :param employer_name: название искомого работодателя
        :return:
            is_ok: bool - успешность
            result: str - полученный URL или описание ошибки
        """
        self.command = 'https://api.hh.ru/employers/'
        self.params = {'text': employer_name,
                       'only_with_vacancies': True,
                       'sort_by': 'by_vacancies_open'}
        is_ok, result = self.make_request()
        self.params.clear()

        if is_ok and result['found']:
            return True, result['items'][0]['url']
        else:
            return False, result

    def get_employer_profile(self, employer_name: str) -> (bool, dict | str):
        """
        Получаем с ХХ профиль искомого работодателя
        :param employer_name: название искомого работодателя
        :return:
            is_ok: bool - успешность
            result: dict | str - полученный профиль или описание ошибки
        """
        is_ok, result = self.get_employer_profile_url(employer_name)

        if is_ok:
            self.command = result
            is_ok, result = self.make_request()
            if is_ok:
                return True, result
            else:
                return False, result
        else:
            return False, result

    def get_vacancies(self, employer_id: str) -> (bool, list | str):
        """
        Получаем с ХХ список вакансий для переданного работодателя
        Параметры:
            Максимальная длина списка - 50 записей,
            Только записи с указанной ЗП
            Сортировка по уменьшению ЗП
        :param employer_id: ID работодателя в ХХ
        :return:
            is_ok: bool - успешность
            result: list | str - полученный список вакансий или описание ошибки
        """
        self.command = 'https://api.hh.ru/vacancies/'
        self.params = {'employer_id': employer_id,
                       'page': 0,
                       'per_page': 50,
                       'only_with_salary': True,
                       'order_by': 'salary_desc'}
        is_ok, result = self.make_request()
        self.params.clear()

        if is_ok:
            return True, result['items']
        else:
            return False, result

    def make_request(self) -> (bool, list | dict | str):
        """
        Выполнение запроса
        Проверка статуса ответа
        :return:
            is_ok: bool - успешность
            result: list | dict | str - полученный результат или описание ошибки
        """
        result = requests.get(self.command, params=self.params)
        answer = result.json()

        if result.status_code != 200:
            return False, answer['errors']

        return True, answer
