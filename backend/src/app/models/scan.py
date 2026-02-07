from pydantic import BaseModel, Field
from app.models.user import SexEnum


class ScanResponse(BaseModel):
    first_name: str
    last_name: str  # alias «Last name» для фронта
    middle_name: str | None
    sex: SexEnum
    birthday: str              # dd:mm:yy
    passport_series: int
    passport_number: int
    passport_issue_date: str   # dd:mm:yy
    passport_expiry_date: str | None
    passport_issuer: str