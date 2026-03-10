from typing import List, Optional, Tuple

from psycopg2.extensions import connection as pg_connection


class DBManager:
    """Класс работы с БД"""

    def __init__(self, conn: pg_connection) -> None:
        self.conn = conn

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Функция получения списка всех компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT e.name, COUNT(v.vacancy_id)
                        FROM employers e
                        JOIN vacancies v ON e.employer_id = v.employer_id
                        GROUP BY e.name
                        ORDER BY count DESC
                    """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, Optional[int], Optional[int], Optional[str], str]]:
        """Функция получения списка всех вакансий с данными."""
        with self.conn.cursor() as cur:
            cur.execute("""
                        SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency, v.url
                        FROM vacancies v
                        JOIN employers e ON v.employer_id = e.employer_id
                    """)
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Функция получения средней зарплаты по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute("""
                    SELECT AVG(
                        CASE
                            WHEN salary_from > 0 AND salary_to > 0 THEN (salary_from + salary_to) / 2
                            WHEN salary_from > 0 THEN salary_from
                            WHEN salary_to > 0 THEN salary_to
                        END
                    )
                    FROM vacancies
                    WHERE (salary_from > 0 OR salary_to > 0)
                      AND (salary_from IS NOT NULL OR salary_to IS NOT NULL)
                """)
            result = cur.fetchone()
            return float(result[0]) if result and result[0] is not None else 0.0

    def get_vacancies_with_higher_salary(
        self,
    ) -> List[Tuple[str, str, Optional[int], Optional[int], Optional[str], str]]:
        """Функция получения списка всех вакансий, у которых зарплата выше средней."""
        avg = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                    SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE
                        CASE
                            WHEN v.salary_from > 0 AND v.salary_to > 0 THEN (v.salary_from + v.salary_to) / 2
                            WHEN v.salary_from > 0 THEN v.salary_from
                            WHEN v.salary_to > 0 THEN v.salary_to
                        END > %s
                """,
                (avg,),
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """Функция получения списка всех вакансий по ключевому слову."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                    SELECT e.name, v.name, v.salary_from, v.salary_to, v.currency, v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.employer_id
                    WHERE v.name ILIKE %s
                """,
                (f"%{keyword}%",),
            )
            return cur.fetchall()
