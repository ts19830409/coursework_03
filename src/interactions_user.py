import datetime
from typing import Optional


def times() -> str:
    """Функция определения времени суток"""
    now = datetime.datetime.now()

    if 6 <= now.hour < 12:
        return "Доброе утро"
    elif 12 <= now.hour < 18:
        return "Добрый день"
    elif 18 <= now.hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def correct_numbers(text: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """Вспомогательная функция для чисел"""
    while True:
        user_input = input(text).strip()
        if user_input.isdigit():
            page_num = int(user_input)
            if min_val is not None and max_val is not None:
                if min_val <= page_num <= max_val:
                    return page_num
                else:
                    print(f"Введите число от {min_val} до {max_val}")
        else:
            print(f"{user_input} не является числом")
