from __future__ import annotations

from typing import Literal, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.models.user import User, ContactInfo


class PolicyInfo(BaseModel):
    title: str
    amount: float


class PolicyDraftSaveReq(BaseModel):
    """Запрос на сохранение черновика (кнопка 'К оплате')."""

    employee_tab_number: str
    arrived_for_hire: bool = False
    lang: Optional[str] = None
    policy_variant: Optional[str] = None  # 'basic' | 'extended'

    user: User
    contacts: ContactInfo
    policy: PolicyInfo


class PolicyDraftSaveResp(BaseModel):
    policy_id: int


class PayInitReq(BaseModel):
    """Инициализация оплаты для уже сохранённого policy_id."""

    policy_id: int
    session_id: UUID = Field(default_factory=uuid4)
    idempotency_key: UUID = Field(default_factory=uuid4)


class PayInitResp(BaseModel):
    session_id: UUID
    amount: float
    currency: str = "RUB"


class PayStatusResp(BaseModel):
    session_id: UUID
    status: Literal["pending", "success", "failed"]
    tx_id: Optional[str] = None


class PayCallback(BaseModel):
    session_id: UUID
    tx_id: str
    status: Literal["success", "failed"]
