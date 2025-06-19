from typing import Optional
from pydantic import BaseModel, Field
from app.models.user import User, ContactInfo
from app.models.payment import PolicyInfo

class RegisterUser(BaseModel):
    user: User
    contacts: ContactInfo
    policy: PolicyInfo
    tx_id: Optional[str] = Field(
        None, alias="transaction id", description="ID of the transaction"
    )
