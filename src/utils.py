def utils_parse_employer(source_employers_profile: dict) -> dict:
    employers_profile = {'id': source_employers_profile['id'],
                         'name': source_employers_profile['name'],
                         'description': source_employers_profile['description']}
    return employers_profile


def utils_parse_vacancies(source_vacancies_list: list, employer_id: str) -> list[dict]:
    vacancies_list = []
    for i in source_vacancies_list:
        if i['salary']['from']:
            vacancy = {'id': i['id'],
                       'employer_id': employer_id,
                       'name': i['name'],
                       'requirement': i['snippet']['requirement'],
                       'responsibility': i['snippet']['responsibility'],
                       'salary_from': i['salary']['from'],
                       'url': i['alternate_url']}
            vacancies_list.append(vacancy)
    return vacancies_list
