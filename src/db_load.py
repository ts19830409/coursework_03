from typing import Dict, List

from psycopg2.extensions import connection as pg_connection


def insert_companies(conn: pg_connection, companies_data: List[Dict]) -> None:
    """Загрузка компаний в таблицу employers"""
    with conn.cursor() as cur:
        for company in companies_data:
            cur.execute(
                """
                INSERT INTO employers (employer_id, name, open_vacancies, url)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING
            """,
                (company["employer_id"], company["name"], company.get("open_vacancies", 0), company.get("url")),
            )

        conn.commit()


def insert_vacancies(conn: pg_connection, vacancies_data: List[Dict]) -> None:
    """Загрузка вакансий в таблицу vacancies"""

    with conn.cursor() as cur:
        for vac in vacancies_data:
            cur.execute(
                """
                    INSERT INTO vacancies (
                        vacancy_id, employer_id, name,
                        salary_from, salary_to, currency, url, requirement, published_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING
                """,
                (
                    vac["vacancy_id"],
                    vac["employer_id"],
                    vac["name"],
                    vac.get("salary_from"),
                    vac.get("salary_to"),
                    vac.get("currency"),
                    vac["url"],
                    vac.get("requirement"),
                    vac["published_at"],
                ),
            )

        conn.commit()
