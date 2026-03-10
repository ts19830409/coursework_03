from typing import Any, Dict, List

from src.class_api import HHAPI


def employer_info_db(employer_list: list) -> List[Dict[str, Any]]:
    """Функция подготовки данных о компаниях к загрузке в БД"""

    hh_api = HHAPI()

    company_db = []

    for name in employer_list:
        raw_company = hh_api.get_employer_info(name)

        if raw_company:
            prepared = {
                "employer_id": raw_company["id"],
                "name": raw_company["name"],
                "open_vacancies": raw_company.get("open_vacancies", 0),
                "url": raw_company.get("alternate_url"),
            }
            company_db.append(prepared)

    return company_db


def dict_of_company(company_db: list) -> Dict[str, str]:
    """Функция получения ID и название организации в словарь"""

    companies_dict = {}
    for company in company_db:
        companies_dict[company["employer_id"]] = company["name"]

    return companies_dict


def load_vacancies_api(company_dict: dict) -> List[Dict[str, Any]]:
    """Функция получения данных о вакансиях согласно списку"""
    hh_api = HHAPI()
    all_raw_vacancies = []

    for employer_id in company_dict.keys():

        raw = hh_api.get_employer_vacancies(employer_id)
        all_raw_vacancies.extend(raw)

    clean_vacancies = vacancies_for_db(all_raw_vacancies)
    return clean_vacancies


def vacancies_for_db(raw_vacancies: List[Dict]) -> List[Dict[str, Any]]:
    """Отбираем только нужные поля для БД"""
    prepared = []

    for vac in raw_vacancies:
        salary = vac.get("salary") or {}
        snippet = vac.get("snippet") or {}

        prepared.append(
            {
                "vacancy_id": vac["id"],
                "name": vac["name"],
                "employer_id": vac["employer"]["id"],
                "salary_from": salary.get("from"),
                "salary_to": salary.get("to"),
                "currency": salary.get("currency"),
                "url": vac["alternate_url"],
                "requirement": snippet.get("requirement"),
                "published_at": vac["published_at"],
            }
        )

    return prepared
