import sys

from api_libs.api_hh import HhAPI


def get_vacancies_from_hh(employers: list) -> (bool, list | str):
    hh_api = HhAPI()
    source_vacancies_list = []
    for i in employers:
        is_ok, result = hh_api.get_employer_id(i)
        if is_ok:
            is_ok, result = hh_api.get_vacancies(result)
            if is_ok:
                source_vacancies_list.append(result)
            else:
                return False, result
        else:
            return False, result
    return True, source_vacancies_list


def parse_vacancies(source_vacancies_list: list) -> list[dict]:
    vacancies_list = []
    for i in source_vacancies_list:
        pass
    return vacancies_list


def init_db(config: dict) -> (bool, str):
    pass


def fill_db(vacancies_list: list) -> (bool, str):
    pass


def make_request(params: list) -> (bool, list | str):
    pass


def print_error(error: str):
    print(error)
    sys.exit()
