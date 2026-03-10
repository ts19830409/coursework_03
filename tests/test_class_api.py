from unittest.mock import MagicMock, patch

from src.class_api import HHAPI


@patch("src.class_api.requests.get")
def test_get_employer_info_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"items": [{"id": "123", "name": "ТестКомпания", "open_vacancies": 10}]}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    api = HHAPI()
    result = api.get_employer_info("Тест")
    assert result is not None
    assert result["id"] == "123"
    assert result["name"] == "ТестКомпания"


@patch("src.class_api.requests.get")
def test_get_employer_info_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"items": []}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    api = HHAPI()
    result = api.get_employer_info("Неизвестная")
    assert result is None


@patch("src.class_api.requests.get")
def test_get_employer_vacancies(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"items": [{"id": "1", "name": "Вакансия 1"}], "found": 1, "pages": 1}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    api = HHAPI()
    result = api.get_employer_vacancies("123")
    assert len(result) == 1
    assert result[0]["id"] == "1"


@patch("src.class_api.requests.get")
def test_get_employer_info_exception(mock_get):
    mock_get.side_effect = Exception("Network error")
    api = HHAPI()
    result = api.get_employer_info("Тест")
    assert result is None


@patch("src.class_api.requests.get")
def test_get_employer_vacancies_no_id(mock_get):
    api = HHAPI()
    result = api.get_employer_vacancies("")
    assert result == []


@patch("src.class_api.requests.get")
def test_get_employer_vacancies_empty_response(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"items": []}
    mock_get.return_value = mock_response

    api = HHAPI()
    result = api.get_employer_vacancies("123")
    assert result == []
