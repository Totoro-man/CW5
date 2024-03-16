from src.processor import *


def main():
    employers = ['Газпром', 'Ямал СПГ', 'Роснефть', 'Лукойл', 'Новатэк',
                 'Норильский никель', 'Татнефть', 'Сахалинская энергия', 'Сбер', 'Фосагро']

    db_config = {
        'user': 'postgres',
        'password': 'admin',
        'host': 'localhost',
        'port': '5432',
        'new_db_name': 'cw5'
    }

    is_ok, result = init_db(db_config)
    if not is_ok:
        error_handling(result)
    else:
        print('БД успешно создана')

    is_ok, result = get_vacancies_from_hh(employers)
    if not is_ok:
        error_handling(result)
    else:
        print('Данные о вакансиях успешно получены')

    vacations_list = parse_vacancies(result)
    print('Данные о вакансиях успешно обработаны')

    is_ok, result = fill_db(vacations_list)
    if not is_ok:
        error_handling(result)
    else:
        print('Данные о вакансиях успешно добавлены в БД')


if __name__ == "__main__":
    main()
