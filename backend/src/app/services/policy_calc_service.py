from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional, Union

PremiumResult = Union[float, str, None]


def full_years(birthday: date, today: date) -> int:
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


@dataclass
class PolicyComputed:
    policy_number: str
    employee_tab_number: str
    insured_full_name: str
    birthday: date
    document_number: str
    issue_date: date
    arrival_purpose: str
    start_date: date
    end_date: date
    insurance_days: int
    premium_total: float


def premium_from_excel_formula(
    *,
    arrival_purpose: str,
    birthday: Optional[date],
    issue_date: Optional[date],
) -> PremiumResult:
    if not arrival_purpose or birthday is None or issue_date is None:
        return None

    try:
        age = full_years(birthday, issue_date)
    except Exception:
        return None

    if age < 0:
        return None

    purpose = arrival_purpose.strip().lower()

    if purpose == "работа" and (age >= 65 or age < 18):
        return "Замени цель приезда"

    if purpose == "работа":
        if 18 <= age < 65:
            return 500.0
        return None

    if purpose == "семья":
        if age < 5:
            return 6000.0
        if 5 <= age < 12:
            return 3000.0
        if 12 <= age < 65:
            return 1500.0
        if 65 <= age < 70:
            return 3000.0
        if 70 <= age < 80:
            return 4500.0
        if 80 <= age < 85:
            return 6000.0
        if age >= 85:
            return 7500.0

    return None


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
    seq: int = 1,
) -> PolicyComputed:
    today = date.today()
    issue_date = today

    start = start_date or today
    end = end_date or (start + timedelta(days=364))
    insurance_days = (end - start).days + 1

    full_name = " ".join(x for x in [last_name, first_name, middle_name] if x)
    document_number = f"{passport_series} {passport_number}".strip()

    # Цель приезда как в Excel
    age = full_years(birthday, issue_date)
    if arrived_for_hire and (18 <= age < 65):
        arrival_purpose = "Работа"
    else:
        arrival_purpose = "Семья"

    premium_res = premium_from_excel_formula(
        arrival_purpose=arrival_purpose,
        birthday=birthday,
        issue_date=issue_date,
    )

    if premium_res is None:
        # Excel вернул бы "" — но нам нужно число.
        # Можно либо 0.0, либо кидать ошибку. Я сделаю явную ошибку:
        raise ValueError("Невозможно рассчитать премию: не хватает данных/некорректный возраст")

    if isinstance(premium_res, str):
        # "Замени цель приезда"
        raise ValueError(premium_res)

    premium_total = float(premium_res)

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
        premium_total=round(premium_total, 2),
    )
