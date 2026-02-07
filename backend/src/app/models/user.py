from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, field_validator


class SexEnum(str, Enum):
    male = "male"
    female = "female"


class ContactInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    email: str = Field(..., alias="email")
    phone_number: str = Field(..., alias="phone number")


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    first_name: str = Field(..., alias="first name")
    last_name: str = Field(..., alias="last name")
    middle_name: Optional[str] = Field(None, alias="middle name")
    sex: SexEnum = Field(..., alias="sex")
    birthday: datetime = Field(..., alias="birthday", description="Format: yyyy-mm-dd")
    passport_series: int = Field(..., alias="passport series")
    passport_number: int = Field(..., alias="passport number")
    passport_issue_date: datetime = Field(
        ..., alias="passport issue date", description="Format: yyyy-mm-dd"
    )
    passport_expiry_date: Optional[datetime] = Field(
        None, alias="passport expiry date", description="Format: yyyy-mm-dd"
    )
    passport_issuer: str = Field(..., alias="passport issuer")
    create_date: datetime = Field(
        default_factory=datetime.now,
        alias="create date",
        description="Format: yyyy-mm-dd",
    )

    @field_validator("birthday", "passport_issue_date", mode="before")
    def validate_date_format(cls, v):
        if isinstance(v, datetime):
            return v
        try:
            return datetime.strptime(v, "%Y-%m-%d")
        except (ValueError, TypeError):
            raise ValueError("Date must be in format yyyy-mm-dd")

    @field_validator("sex", mode="after")
    def convert_sex_enum_to_str(cls, v: SexEnum) -> str:
        return v.value

    @property
    def birthday_str(self) -> str:
        return self.birthday.strftime("%Y-%m-%d")

    @property
    def passport_issue_date_str(self) -> str:
        return self.passport_issue_date.strftime("%Y-%m-%d")
