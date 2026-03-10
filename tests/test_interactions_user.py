from unittest.mock import patch

from src.interactions_user import correct_numbers, times


def test_times():
    with patch("src.interactions_user.datetime") as mock_dt:
        mock_dt.datetime.now.return_value.hour = 10
        assert times() == "Доброе утро"

        mock_dt.datetime.now.return_value.hour = 15
        assert times() == "Добрый день"

        mock_dt.datetime.now.return_value.hour = 20
        assert times() == "Добрый вечер"

        mock_dt.datetime.now.return_value.hour = 3
        assert times() == "Доброй ночи"


@patch("builtins.input")
def test_correct_numbers_valid(mock_input):
    mock_input.side_effect = ["5"]
    result = correct_numbers("Введите число: ", 1, 10)
    assert result == 5


@patch("builtins.input")
def test_correct_numbers_invalid_then_valid(mock_input):
    mock_input.side_effect = ["abc", "15", "7"]
    result = correct_numbers("Введите число: ", 1, 10)
    assert result == 7
