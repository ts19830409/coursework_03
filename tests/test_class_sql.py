from unittest.mock import MagicMock

import pytest

from src.class_sql import DBManager


@pytest.fixture
def db_manager():
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur
    return DBManager(mock_conn), mock_cur


def test_get_companies_and_vacancies_count(db_manager):
    db, mock_cur = db_manager
    mock_cur.fetchall.return_value = [("Компания А", 10), ("Компания Б", 5)]

    result = db.get_companies_and_vacancies_count()
    assert len(result) == 2
    assert result[0][1] == 10
    mock_cur.execute.assert_called_once()


def test_get_avg_salary(db_manager):
    db, mock_cur = db_manager
    mock_cur.fetchone.return_value = (75000,)

    result = db.get_avg_salary()
    assert result == 75000


def test_get_vacancies_with_keyword(db_manager):
    db, mock_cur = db_manager
    mock_cur.fetchall.return_value = [("Компания", "Python dev", 100, 200, "RUR", "url")]

    result = db.get_vacancies_with_keyword("python")
    assert len(result) == 1
    assert "Python" in result[0][1]


def test_get_avg_salary_no_data():
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchone.return_value = (None,)
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    db = DBManager(mock_conn)
    result = db.get_avg_salary()
    assert result == 0


def test_get_vacancies_with_higher_salary_no_data():
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_cur.fetchall.return_value = []
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    db = DBManager(mock_conn)
    result = db.get_vacancies_with_higher_salary()
    assert result == []
