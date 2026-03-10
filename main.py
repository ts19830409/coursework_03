from typing import List, Optional, Tuple

from colorama import Fore, Style, init
from psycopg2 import connect

from src.class_sql import DBManager
from src.config import employer_list
from src.db_create import config, create_company_tables, create_db, create_vacancies_tables
from src.db_load import insert_companies, insert_vacancies
from src.interactions_user import correct_numbers, times
from src.utils import dict_of_company, employer_info_db, load_vacancies_api

init()


def user_menu() -> None:
    """Функция главного меню"""

    times_of_day = times()
    print(f"\n{times_of_day}, Уважаемый пользователь!")
    print(f'{Fore.CYAN}Вас приветствует программа: "Поиск вакансий с подключением БД"{Style.RESET_ALL}\n')
    print("Ждите, идет загрузка данных... ")

    conn = create_db()
    create_company_tables(conn)

    create_vacancies_tables(conn)

    companies_data = employer_info_db(employer_list)
    insert_companies(conn, companies_data)

    companies_dict = dict_of_company(companies_data)
    clean_vacancies = load_vacancies_api(companies_dict)

    insert_vacancies(conn, clean_vacancies)

    conn.close()

    print("Загрузка завершена")
    params = config()
    conn = connect(dbname="hhru", **params)  # type: ignore[call-overload]
    db = DBManager(conn)

    while True:
        print("""
            1. Список всех компаний и количество вакансий у каждой компании
            2. Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
            3. Средняя зарплата по вакансиям
            4. Список всех вакансий, у которых зарплата выше средней по всем вакансиям
            5. Список всех вакансий, в названии которых содержатся переданные в метод слова
            6. Выход их программы
            """)

        choice_data = correct_numbers("Выберите пункт, введя число от 1 до 6: \n", 1, 6)

        if choice_data == 1:
            results: List[Tuple[str, int]] = db.get_companies_and_vacancies_count()
            for company, count in results:
                print(f"{company}: {count} вакансий")
            input("\nНажмите Enter для продолжения...")

        elif choice_data == 2:
            results_all: List[Tuple[str, str, Optional[int], Optional[int], Optional[str], str]] = (
                db.get_all_vacancies()
            )
            print(f"Всего вакансий: {len(results_all)}")
            for i, (company, vac, sal_from, sal_to, cur, url) in enumerate(results_all[:15], 1):
                print(f"{i}. {company} | {vac} | {sal_from}-{sal_to} {cur} | {url}")
            print("... и ещё", len(results_all) - 15)
            input("\nНажмите Enter для продолжения...")

        elif choice_data == 3:
            avg = db.get_avg_salary()
            print(f"Средняя зарплата: {avg:.2f}")
            input("\nНажмите Enter для продолжения...")

        elif choice_data == 4:

            results_high: List[Tuple[str, str, Optional[int], Optional[int], Optional[str], str]] = (
                db.get_vacancies_with_higher_salary()
            )

            print(f"Всего вакансий с зарплатой выше средней: {len(results_high)}")

            for i, (company, vac, sal_from, sal_to, cur, url) in enumerate(results_high[:15], 1):
                print(f"{i}. {company} | {vac} | {sal_from or '?'}-{sal_to or '?'} {cur or ''}".strip("- "))

            print("... и ещё", len(results_high) - 15)

            input("\nНажмите Enter для продолжения...")

        elif choice_data == 5:

            keyword = input("Введите ключевое слово: ")

            results_search: List[Tuple[str, str, Optional[int], Optional[int], Optional[str], str]] = (
                db.get_vacancies_with_keyword(keyword)
            )

            print(f"Найдено вакансий с '{keyword}': {len(results_search)}")

            if results_search:

                for company, vac, sal_from, sal_to, cur, url in results_search[:15]:
                    print(f"{company} | {vac} | {sal_from}-{sal_to} {cur}")

                if len(results_search) > 15:
                    print("... и ещё", len(results_search) - 15)

            else:

                print("Ничего не найдено.")

            input("\nНажмите Enter для продолжения...")

        elif choice_data == 6:
            break


if __name__ == "__main__":
    user_menu()
