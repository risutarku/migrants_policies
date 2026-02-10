from __future__ import annotations

from datetime import date
from pydantic import BaseModel


class UserIn(BaseModel):
    # Важно: backend ожидает first_name, last_name...
    first_name: str
    last_name: str
    middle_name: str | None = None
    birthday: date
    passport_series: str
    passport_number: str


class ContactsIn(BaseModel):
    email: str | None = None


class PolicyIn(BaseModel):
    title: str
    price: float


class CreatePolicyReq(BaseModel):
    employee_tab_number: str
    arrived_for_hire: bool = False
    user: UserIn
    contacts: ContactsIn | None = None
    policy: PolicyIn


class CreatePolicyResp(BaseModel):
    policy_id: int
    status: str


class PolicyOut(BaseModel):
    id: int
    status: str
    employee_tab_number: str
    arrived_for_hire: bool
    first_name: str
    last_name: str
    middle_name: str | None
    birthday: date
    passport_series: str
    passport_number: str
    contacts_email: str | None
    policy_title: str
    price: float

    policy_number: str | None
    issue_date: date | None
    start_date: date | None
    end_date: date | None
    insurance_days: int | None
    arrival_purpose: str | None
    reward_amount: float | None
    xlsx_path: str | None

    class Config:
        from_attributes = True


class MarkPaidReq(BaseModel):
    tx_id: str | None = None


class IssueReq(BaseModel):
    # если даты задаются не всегда — можно оставить пустыми и считать по умолчанию
    start_date: date | None = None
    end_date: date | None = None
