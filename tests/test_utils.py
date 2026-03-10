from unittest.mock import MagicMock, patch

from src.utils import dict_of_company, employer_info_db, load_vacancies_api, vacancies_for_db


def test_dict_of_company():
    company_db = [{"employer_id": "123", "name": "Компания А"}, {"employer_id": "456", "name": "Компания Б"}]
    result = dict_of_company(company_db)
    assert result == {"123": "Компания А", "456": "Компания Б"}


def test_vacancies_for_db():
    raw_vacancies = [
        {
            "id": "1",
            "name": "Вакансия",
            "employer": {"id": "123"},
            "salary": {"from": 100, "to": 200, "currency": "RUR"},
            "alternate_url": "https://hh.ru/1",
            "snippet": {"requirement": "Требования"},
            "published_at": "2024-01-01",
        }
    ]
    result = vacancies_for_db(raw_vacancies)
    assert len(result) == 1
    assert result[0]["vacancy_id"] == "1"
    assert result[0]["salary_from"] == 100


# 1. employer_info_db — если компания не найдена
@patch("src.utils.HHAPI")
def test_employer_info_db_no_company(mock_hhapi):
    mock_api = MagicMock()
    mock_api.get_employer_info.return_value = None
    mock_hhapi.return_value = mock_api

    result = employer_info_db(["Неизвестная компания"])
    assert result == []


# 2. employer_info_db — пустой список на входе
def test_employer_info_db_empty_list():
    result = employer_info_db([])
    assert result == []


# 3. load_vacancies_api — пустой словарь
@patch("src.utils.HHAPI")
def test_load_vacancies_api_empty_dict(mock_hhapi):
    result = load_vacancies_api({})
    assert result == []


# 4. load_vacancies_api — API вернул пустой список
@patch("src.utils.HHAPI")
def test_load_vacancies_api_no_vacancies(mock_hhapi):
    mock_api = MagicMock()
    mock_api.get_employer_vacancies.return_value = []
    mock_hhapi.return_value = mock_api

    result = load_vacancies_api({"123": "Компания"})
    assert result == []


# 5. vacancies_for_db — salary = None
def test_vacancies_for_db_no_salary():
    raw = [
        {
            "id": "1",
            "name": "Вакансия",
            "employer": {"id": "123"},
            "salary": None,
            "alternate_url": "url",
            "snippet": None,
            "published_at": "2024-01-01",
        }
    ]
    result = vacancies_for_db(raw)
    assert len(result) == 1
    assert result[0]["salary_from"] is None
    assert result[0]["requirement"] is None


# 6. vacancies_for_db — snippet пустой
def test_vacancies_for_db_no_snippet():
    raw = [
        {
            "id": "1",
            "name": "Вакансия",
            "employer": {"id": "123"},
            "salary": {"from": 100},
            "alternate_url": "url",
            "snippet": {},
            "published_at": "2024-01-01",
        }
    ]
    result = vacancies_for_db(raw)
    assert result[0]["requirement"] is None


# 7. vacancies_for_db — несколько вакансий
def test_vacancies_for_db_multiple():
    raw = [
        {
            "id": "1",
            "name": "A",
            "employer": {"id": "1"},
            "salary": {},
            "alternate_url": "u1",
            "snippet": {},
            "published_at": "t1",
        },
        {
            "id": "2",
            "name": "B",
            "employer": {"id": "2"},
            "salary": {},
            "alternate_url": "u2",
            "snippet": {},
            "published_at": "t2",
        },
    ]
    result = vacancies_for_db(raw)
    assert len(result) == 2


# 8. dict_of_company — пустой список
def test_dict_of_company_empty():
    result = dict_of_company([])
    assert result == {}


# 9. dict_of_company — один элемент
def test_dict_of_company_single():
    data = [{"employer_id": "123", "name": "Тест"}]
    result = dict_of_company(data)
    assert result == {"123": "Тест"}
