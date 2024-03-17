import sys

from src.api_hh import HhAPI
from src.db import Db
from src.utils import *


def get_employers_profiles(employers: list) -> (bool, list | str):
    """
    Получаем список профилей необходимых нам работодателей
    :param employers: список работодателей
    :return:
        is_ok: bool - успешность
        result: list | str - полученный список или описание ошибки
    """
    hh_api = HhAPI()
    employers_profiles_list = []
    for i in employers:
        is_ok, result = hh_api.get_employer_profile(i)
        if is_ok:
            employer_profile = utils_parse_employer(result)
            employers_profiles_list.append(employer_profile)
        else:
            return False, result
    del hh_api
    return True, employers_profiles_list


def get_vacancies(employers: list) -> (bool, list | str):
    """
    Получаем список вакансий необходимых нам работодателей
    :param employers: список профилей работодателей
    :return:
        is_ok: bool - успешность,
        result: list | str - полученный список или описание ошибки
    """
    hh_api = HhAPI()
    vacancies_list = []
    for i in employers:
        is_ok, result = hh_api.get_vacancies(i['id'])
        if is_ok:
            i_vacancies_list = utils_parse_vacancies(result, i['id'])
            vacancies_list.extend(i_vacancies_list)
        else:
            return False, result
    del hh_api
    return True, vacancies_list


def db_init_db(config: dict, file_path: str) -> (bool, str):
    config2 = config.copy()
    new_db_name = config2.pop('dbname')
    db = Db(config2, new_db_name)
    db.init_database()
    db = Db(config)
    db.execute_sql_from_file(file_path)
    db.stop()
    del db
    return True, 'All OK'


def db_insert_employers(config: dict, employers_list: list) -> (bool, str):
    db = Db(config)
    for i in employers_list:
        query = (f'INSERT INTO employers ({', '.join(list(i.keys()))}) '
                 f'VALUES ({i['id']}, \'{i['name']}\', \'{i['description']}\')')
        db.send_request(query)
    db.stop()
    del db
    return True, 'All OK'


def db_insert_vacancies(config: dict, vacancies_list: list) -> (bool, str):
    db = Db(config)
    for i in vacancies_list:
        query = (f'INSERT INTO vacancies ({', '.join(list(i.keys()))}) '
                 f'VALUES ({i['id']}, {i['employer_id']}, \'{i['name']}\', \'{i['requirement']}\','
                 f'\'{i['responsibility']}\', {i['salary_from']}, \'{i['url']}\')')
        db.send_request(query)
    db.stop()
    del db
    return True, 'All OK'


def make_cw5_requests(config: dict):
    db = Db(config)
    db.get_companies_and_vacancies_count()
    db.get_all_vacancies()
    db.get_avg_salary()
    db.get_vacancies_with_higher_salary()
    db.get_vacancies_with_keywords(['едущий', 'лавный'])
    db.stop()
    del db


def error_handling(error: str):
    print(error)
    sys.exit()
