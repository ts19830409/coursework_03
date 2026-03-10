from configparser import ConfigParser
from typing import Dict, cast

import psycopg2
from psycopg2.extensions import connection


def config(filename: str = "database.ini", section: str = "postgresql") -> Dict[str, str]:
    """Функция чтения параметров подключения к БД из .ini файла"""
    parser = ConfigParser()
    parser.read(filename)

    db_params: Dict[str, str] = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in {filename}")

    return db_params


def create_db() -> connection:
    """Функция создания БД"""
    params = config()
    conn = cast(connection, psycopg2.connect(dbname="postgres", **params))  # type: ignore[call-overload]

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'hhru'
        AND pid <> pg_backend_pid()
    """)

    cur.execute("DROP DATABASE IF EXISTS hhru")
    cur.execute("CREATE DATABASE hhru")

    cur.close()
    conn.close()

    conn = cast(connection, psycopg2.connect(dbname="hhru", **params))  # type: ignore[call-overload]
    return conn


def create_company_tables(conn: connection) -> None:
    """Функция создания таблицы организаций"""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                open_vacancies INTEGER DEFAULT 0,
                url TEXT
            )
        """)
        conn.commit()


def create_vacancies_tables(conn: connection) -> None:
    """Функция создания таблицы вакансий"""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id VARCHAR(50) PRIMARY KEY,
                employer_id VARCHAR(50) REFERENCES employers(employer_id),
                name VARCHAR(255) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                currency VARCHAR(10),
                url TEXT,
                requirement TEXT,
                published_at TIMESTAMP
            )
        """)
        conn.commit()
