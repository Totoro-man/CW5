from src.processor import *


def main():
    employers = ['Газпром', 'Ямал СПГ', 'Роснефть', 'Лукойл', 'Новатэк',
                 'Норильский никель', 'Татнефть', 'Сахалинская энергия', 'Сбер', 'Фосагро']

    db_config = {
        'user': 'postgres',
        'password': 'admin',
        'host': 'localhost',
        'port': '5432',
        'dbname': 'cw5'
    }
    sql_scripts_file_path = 'src/queries.sql'

    is_ok, result = db_init_db(db_config, sql_scripts_file_path)
    if not is_ok:
        error_handling(result)
    else:
        print('БД успешно создана')

    is_ok, employers_profiles_list = get_employers_profiles(employers)
    if not is_ok:
        error_handling(employers_profiles_list)
    else:
        print('Данные о работодателях успешно получены')

    is_ok, result = db_insert_employers(db_config, employers_profiles_list)
    if not is_ok:
        error_handling(result)
    else:
        print('Данные о работодателях успешно добавлены в БД')

    is_ok, vacancies_list = get_vacancies(employers_profiles_list)
    if not is_ok:
        error_handling(vacancies_list)
    else:
        print('Данные о вакансиях успешно получены')

    is_ok, result = db_insert_vacancies(db_config, vacancies_list)
    if not is_ok:
        error_handling(result)
    else:
        print('Данные о вакансиях успешно добавлены в БД')

    # is_ok, result = db_fill_db(result)
    # if not is_ok:
    #     error_handling(result)
    # else:
    #     print('Данные о вакансиях успешно добавлены в БД')


if __name__ == "__main__":
    main()

