from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.policy import Policy


@dataclass
class PaymentRecord:
    status: str = "pending"  # pending|success|failed
    tx_id: Optional[str] = None
    policy_id: Optional[int] = None
    amount: float = 0.0
    idempotency_key: Optional[UUID] = None


class InMemoryPayStore:
    """Простой in-memory store для имитации терминала в dev.

    В проде это обычно заменяется внешним платёжным шлюзом.
    """

    def __init__(self):
        self._store: Dict[str, PaymentRecord] = {}
        # policy_id -> amount (чтобы /payment/init мог взять сумму без доп. запроса к БД)
        self._policy_amount: Dict[int, float] = {}

    def remember_policy_amount(self, policy_id: int, amount: float) -> None:
        self._policy_amount[int(policy_id)] = float(amount)

    def get_policy_amount(self, policy_id: int) -> Optional[float]:
        return self._policy_amount.get(int(policy_id))

    def create(self, session_id: UUID, idempotency_key: UUID, amount: float) -> UUID:
        sid = session_id
        self._store[str(sid)] = PaymentRecord(
            status="pending",
            tx_id=None,
            policy_id=None,
            amount=float(amount),
            idempotency_key=idempotency_key,
        )
        return sid

    def attach_policy(self, session_id: UUID, policy_id: int) -> None:
        rec = self._store.get(str(session_id))
        if not rec:
            self._store[str(session_id)] = PaymentRecord(policy_id=int(policy_id))
        else:
            rec.policy_id = int(policy_id)

    def get(self, session_id: UUID):
        rec = self._store.get(str(session_id))
        if not rec:
            return None
        return {
            "status": rec.status,
            "tx_id": rec.tx_id,
            "policy_id": rec.policy_id,
            "amount": rec.amount,
        }

    def mark(self, session_id: UUID, status: str, tx_id: Optional[str] = None) -> None:
        rec = self._store.get(str(session_id))
        if not rec:
            rec = PaymentRecord()
            self._store[str(session_id)] = rec
        rec.status = status
        rec.tx_id = tx_id

    async def get_amount_for_policy(self, policy_id: int, db: Session) -> float:
        p = db.query(Policy).filter(Policy.id == int(policy_id)).first()
        if not p:
            return 0.0
        return float(p.price)


pay_store = InMemoryPayStore()
