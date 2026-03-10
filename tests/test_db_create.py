from unittest.mock import MagicMock, patch

import pytest

from src.db_create import config, create_db


@patch("src.db_create.ConfigParser")
def test_config_success(mock_config_parser):
    mock_parser = MagicMock()
    mock_parser.has_section.return_value = True
    mock_parser.items.return_value = [("host", "localhost"), ("user", "postgres")]
    mock_config_parser.return_value = mock_parser

    result = config("fake.ini", "postgresql")
    assert result == {"host": "localhost", "user": "postgres"}


@patch("src.db_create.ConfigParser")
def test_config_section_not_found(mock_config_parser):
    mock_parser = MagicMock()
    mock_parser.has_section.return_value = False
    mock_config_parser.return_value = mock_parser

    with pytest.raises(Exception, match="Section test not found"):
        config("fake.ini", "test")


@patch("src.db_create.psycopg2.connect")
def test_create_db(mock_connect):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    mock_connect.return_value = mock_conn

    with patch("src.db_create.config", return_value={"host": "localhost"}):
        conn = create_db()
        assert conn is not None
        mock_cur.execute.assert_any_call("DROP DATABASE IF EXISTS hhru")
        mock_cur.execute.assert_any_call("CREATE DATABASE hhru")
