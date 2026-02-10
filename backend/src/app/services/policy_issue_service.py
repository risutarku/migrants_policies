# from __future__ import annotations

# from dataclasses import dataclass
# from datetime import date, timedelta
# from typing import Optional


# def full_years(birthday: date, today: date) -> int:
#     return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


# @dataclass
# class IssueComputed:
#     policy_number: str
#     issue_date: date
#     start_date: date
#     end_date: date
#     insurance_days: int
#     arrival_purpose: str
#     reward_amount: float
#     insured_full_name: str
#     document_number: str


# def compute_issue_fields(
#     *,
#     db_id: int,
#     arrived_for_hire: bool,
#     employee_tab_number: str,  # сейчас не используется в формулах, но может понадобиться
#     first_name: str,
#     last_name: str,
#     middle_name: Optional[str],
#     birthday: date,
#     passport_series: str,
#     passport_number: str,
#     start_date: Optional[date] = None,
#     end_date: Optional[date] = None,
# ) -> IssueComputed:
#     today = date.today()
#     issue_date = today

#     # Даты полиса (пример: 1 год). Если у тебя другое правило — поменяешь здесь.
#     start = start_date or today
#     end = end_date or (start + timedelta(days=364))
#     insurance_days = (end - start).days + 1

#     age = full_years(birthday, today)
#     if arrived_for_hire and (18 <= age < 65):
#         arrival_purpose = "РАБОТА"
#     else:
#         arrival_purpose = "СЕМЬЯ"

#     # Номер полиса как в Excel-логике: 7000000 + id, "-", месяц выдачи
#     policy_number = f"{7000000 + db_id}-{issue_date.month}"

#     insured_full_name = " ".join(x for x in [last_name, first_name, middle_name] if x)
#     document_number = f"{passport_series} {passport_number}".strip()

#     # Вознаграждение — ВСТАВЬ СВОЮ ФОРМУЛУ
#     # Пример-заглушка:
#     reward_amount = 0.0
#     if arrival_purpose == "РАБОТА":
#         reward_amount = 500.0
#     else:
#         reward_amount = 300.0

#     return IssueComputed(
#         policy_number=policy_number,
#         issue_date=issue_date,
#         start_date=start,
#         end_date=end,
#         insurance_days=insurance_days,
#         arrival_purpose=arrival_purpose,
#         reward_amount=reward_amount,
#         insured_full_name=insured_full_name,
#         document_number=document_number,
#     )
