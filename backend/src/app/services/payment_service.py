import asyncio
import time
from uuid import UUID
from typing import Dict, Optional


from app.services.draft_user_service import draft_store
from app.services.user_service import register_user



async def mock_payment():
    """
    Simulates a payment process by sleeping for 2 seconds and returning a mock transaction ID.
    """
    await asyncio.sleep(2)
    return {"tx_id": "TX-" + str(int(time.time()))}


async def _mock_terminal(sid: UUID):
    await asyncio.sleep(2)
    tx_id = f"TX-{int(time.time())}"
    pay_store.mark(sid, "success", tx_id)
    draft = draft_store.pop(sid)
    if draft:
        register_user(draft, tx_id)


class _InMemPayStore:
    """Mock DB-таблицы draft_user & payment."""
    payments: Dict[UUID, dict] = {}
    idem_index: dict[UUID, UUID] = {}

    def create(self, sid, idem, amount):
        if idem in self.idem_index:
            return self.idem_index[idem]
        self.payments[sid] = {"status": "pending", "amount": amount, "tx_id": None}
        self.idem_index[idem] = sid
        return sid

    @classmethod
    def create_pending(cls, sid: UUID, amount: int):
        cls.payments[sid] = {"status": "pending", "amount": amount, "tx_id": None}

    @classmethod
    def mark(cls, sid: UUID, status: str, tx_id: str | None = None):
        if sid in cls.payments:
            cls.payments[sid].update(status=status, tx_id=tx_id)

    @classmethod
    def get(cls, sid: UUID) -> Optional[dict]:
        return cls.payments.get(sid)

pay_store = _InMemPayStore()
