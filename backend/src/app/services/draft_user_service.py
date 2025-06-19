from uuid import UUID
from typing import Dict, Optional
from app.models.to_csv import RegisterUser

class _DraftMemStore:
    _data: Dict[UUID, RegisterUser] = {}

    @classmethod
    def save(cls, sid: UUID, draft: RegisterUser):
        cls._data[sid] = draft

    @classmethod
    def pop(cls, sid: UUID) -> Optional[RegisterUser]:
        return cls._data.pop(sid, None)

draft_store = _DraftMemStore()
