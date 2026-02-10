from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class SexEnum(str, Enum):
    male = "male"
    female = "female"


def _parse_date(v) -> date:
    """Accepts date or 'YYYY-MM-DD' string."""
    if isinstance(v, date) and not isinstance(v, datetime):
        return v
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, str):
        return datetime.strptime(v, "%Y-%m-%d").date()
    raise ValueError("Date must be in format YYYY-MM-DD")


class ContactInfo(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None


class User(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    sex: Optional[SexEnum] = None

    # используем date (а не datetime), чтобы проще стыковать с БД/формой
    birthday: date

    passport_series: str
    passport_number: str
    passport_issue_date: Optional[date] = None
    passport_expiry_date: Optional[date] = None
    passport_issuer: Optional[str] = None

    @field_validator("birthday", "passport_issue_date", "passport_expiry_date", mode="before")
    @classmethod
    def _v_dates(cls, v):
        if v is None or v == "":
            return None
        return _parse_date(v)
