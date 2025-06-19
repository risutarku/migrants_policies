from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Literal, Optional

from app.models.user import User, ContactInfo


class PolicyInfo(BaseModel):
    title: str = Field(..., alias="title")
    amount: int = Field(..., alias="amount")


class PayInitReq(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    amount: int


class PayInitResp(BaseModel):
    session_id: UUID
    amount: int
    currency: str = "KZT"


class PayStatusResp(BaseModel):
    session_id: UUID
    status: Literal["pending", "success", "failed"]
    tx_id: Optional[str] = None


class PayInitReq(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    user: User
    contacts: ContactInfo
    policy: PolicyInfo
    idempotency_key: UUID = Field(default_factory=uuid4)


class PayCallback(BaseModel):
    session_id: UUID
    tx_id: str
    status: Literal["success", "failed"]
