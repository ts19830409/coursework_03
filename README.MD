## Описание
Поиск вакансий с подключением БД

## Функционал проекта.

### Пакет src

#### Модуль class_api.py
Содержит класс для работы с API:
```
class HHAPI:
```
#### class_sql.py
Класс работы с БД
```
class DBManager:
```
### Модуль config.py
Содержит список организаций

### Модуль db_create.py
Содержит функций для создания БД:
1. Функция чтения параметров подключения к БД из .ini файла:
```
def config(filename: str = "database.ini", section: str = "postgresql") -> Dict[str, str]:
```
2. Функция создания БД:
```
def create_db() -> connection:
```
3. Функция создания таблицы организаций:
```
def create_company_tables(conn: connection) -> None:
```
4. Функция создания таблицы вакансий:
```
def create_vacancies_tables(conn: connection) -> None:
```
### Модуль db_load.py
Содержит функции загрузки данных в БД:  
1. Загрузка компаний в таблицу employers:
```
def insert_companies(conn: pg_connection, companies_data: List[Dict]) -> None:
```
2. Загрузка вакансий в таблицу vacancies:
```
def insert_vacancies(conn: pg_connection, vacancies_data: List[Dict]) -> None:
```
#### Модуль interactions_user.py
Содержит функции для взаимодействия с пользователем:
1. Функция определения времени суток:
```
def times() -> str:
```
2. Вспомогательная функция для чисел:
```
def correct_numbers(text: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
```
#### Модуль utils.py
Содержит функции подготовки данных для таблиц
1. Функция подготовки данных о компаниях к загрузке в БД:
```
def employer_info_db(employer_list: list) -> List[Dict[str, Any]]:
```
2. Функция получения ID и название организации в словарь:
```
def dict_of_company(company_db: list) -> Dict[str, str]:
```
3. Функция получения данных о вакансиях согласно списку:
```
def load_vacancies_api(company_dict: dict) -> List[Dict[str, Any]]:
```
4. Отбираем только нужные поля для БД:
```
def vacancies_for_db(raw_vacancies: List[Dict]) -> List[Dict[str, Any]]:
```
### Пакет tests
Содержит модули test_class_api.py, test_class_sql.py, test_db_create.py, test_db_load.py,
test_interactions_user.py, test_utils.py для тестирования соответствующих модулей.
Тесты написаны с использованием фикстур и параметризации, а так же Mock и patch.

### Модуль main
Содержит функцию пользовательского меню:
1. Основная функция взаимодействия с пользователем:
```
def main_page() -> None:
```
# Установка:
**Клонируйте репозиторий:**
```
https://github.com/ts19830409/coursework_03.git
```
*Проект разработан в рамках курсового проекта*