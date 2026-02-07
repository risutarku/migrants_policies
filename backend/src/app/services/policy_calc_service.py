from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional


def full_years(birthday: date, today: date) -> int:
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


@dataclass
class PolicyComputed:
    # для БД/документа
    policy_number: str
    employee_tab_number: str
    insured_full_name: str
    birthday: date
    document_number: str
    issue_date: date
    arrival_purpose: str
    start_date: date
    end_date: date

    # для Excel
    insurance_days: int
    premium_total: float


def compute_policy(
    *,
    employee_tab_number: str,
    arrived_for_hire: bool,
    last_name: str,
    first_name: str,
    middle_name: Optional[str],
    birthday: date,
    passport_series: str,
    passport_number: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    base_premium: float = 1000.0,
    seq: int = 1,  # ВРЕМЕННО: счетчик для номера полиса, пока без БД
) -> PolicyComputed:
    today = date.today()
    issue_date = today

    # даты страхования (для теста: год)
    start = start_date or today
    end = end_date or (start + timedelta(days=364))
    insurance_days = (end - start).days + 1

    # ФИО
    full_name = " ".join(x for x in [last_name, first_name, middle_name] if x)

    # Документ
    document_number = f"{passport_series} {passport_number}".strip()

    # возраст и цель приезда
    age = full_years(birthday, today)
    if arrived_for_hire and (18 <= age < 65):
        arrival_purpose = "РАБОТА"
    else:
        arrival_purpose = "СЕМЬЯ"

    # премия (пока простая демо-логика)
    premium = float(base_premium)
    if age < 18:
        premium *= 0.8
    elif age >= 65:
        premium *= 1.3
    if arrival_purpose == "РАБОТА":
        premium *= 1.1

    # номер полиса (пока без БД: 7000000 + seq)
    policy_number = f"{7000000 + seq}-{issue_date.month}"

    return PolicyComputed(
        policy_number=policy_number,
        employee_tab_number=employee_tab_number,
        insured_full_name=full_name,
        birthday=birthday,
        document_number=document_number,
        issue_date=issue_date,
        arrival_purpose=arrival_purpose,
        start_date=start,
        end_date=end,
        insurance_days=insurance_days,
        premium_total=round(premium, 2),
    )
