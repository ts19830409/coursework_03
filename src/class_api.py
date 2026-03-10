# mypy: ignore-errors
import time
from typing import Any, Dict, List, Optional

import requests


class HHAPI:
    """Класс для взаимодействия с публичным API"""

    BASE_URL = "https://api.hh.ru"

    def get_employer_info(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Функция для получения информации о компании по её названию."""
        try:
            response = requests.get(
                f"{self.BASE_URL}/employers",
                params={"text": company_name, "per_page": 20, "only_with_vacancies": True},
            )

            response.raise_for_status()
            data = response.json()

            if not data["items"]:
                print(f"Компании '{company_name}' не найдены")
                return None

            companies = sorted(data["items"], key=lambda x: x.get("open_vacancies", 0), reverse=True)

            main_company = companies[0]
            if isinstance(main_company, dict):
                return main_company
            return None

        except Exception as e:
            print(f"Ошибка при поиске компании '{company_name}': {e}")
        return None

    def get_employer_vacancies(self, employer_id: str) -> List[Dict[str, Any]]:
        """Функция получения информации о вакансиях"""
        if not employer_id:
            return []

        all_vacancies = []
        page = 0
        all_page = 100

        while True:
            try:
                response = requests.get(
                    f"{self.BASE_URL}/vacancies",
                    params={"employer_id": employer_id, "page": page, "per_page": all_page},
                    timeout=5,
                )
                response.raise_for_status()
                data = response.json()
                items = data.get("items", [])

                if not items:
                    break

                all_vacancies.extend(items)

                total_found = data.get("found", 0)
                if len(all_vacancies) >= total_found or len(items) < all_page:
                    break

                page += 1
                time.sleep(0.5)

            except Exception as e:
                print(f"Ошибка получения данных для {employer_id}: {e}")
                break

        return all_vacancies
