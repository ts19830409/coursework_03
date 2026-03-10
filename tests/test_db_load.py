from unittest.mock import MagicMock

from src.db_load import insert_companies, insert_vacancies


def test_insert_companies():
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    companies = [{"employer_id": "123", "name": "Тест", "open_vacancies": 10, "url": "https://hh.ru/123"}]

    insert_companies(mock_conn, companies)
    mock_cur.execute.assert_called_once()
    mock_conn.commit.assert_called_once()


def test_insert_vacancies():
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    vacancies = [
        {
            "vacancy_id": "1",
            "employer_id": "123",
            "name": "Вакансия",
            "salary_from": 100,
            "salary_to": 200,
            "currency": "RUR",
            "url": "https://hh.ru/1",
            "requirement": "Тест",
            "published_at": "2024-01-01",
        }
    ]

    insert_vacancies(mock_conn, vacancies)
    mock_cur.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
