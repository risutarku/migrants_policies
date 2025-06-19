from fastapi import APIRouter, HTTPException
import httpx

from app.services.payment_service import mock_payment
from app.exceptions.payment_exceptions import PaymentFailedException
from app.services.user_service import register_user
from app.models.to_csv import RegisterUser

from uuid import UUID
import asyncio, time, random
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.models.payment import PayInitReq, PayInitResp, PayStatusResp
from app.services.payment_service import pay_store
from app.services.draft_user_service import draft_store
from app.models.payment import PayCallback

router = APIRouter()


@router.post("/init", response_model=PayInitResp, status_code=201)
async def payment_init(p: PayInitReq):
    sid = pay_store.create(p.session_id, p.idempotency_key, p.policy.amount)
    draft_store.save(sid, RegisterUser(user=p.user, contacts=p.contacts, policy=p.policy))
    if pay_store.get(sid)['status'] == "pending":
        asyncio.create_task(_mock_terminal(sid))
    return PayInitResp(session_id=sid, amount=p.policy.amount)


async def _mock_terminal(sid: UUID):
    await asyncio.sleep(2)
    tx_id = f"TX-{int(time.time())}-{random.randint(100,999)}"
    async with httpx.AsyncClient() as c:
        await c.post(
            "http://localhost:8000/payment/callback",
            json={"session_id": str(sid), "tx_id": tx_id, "status": "success"},
            timeout=5,
        )


@router.get("/status/{sid}", response_model=PayStatusResp)
async def payment_status(sid: UUID):
    rec = pay_store.get(sid)
    if not rec:
        raise HTTPException(404, "session not found")
    return PayStatusResp(session_id=sid, **rec)


@router.post("/callback", status_code=204)
async def payment_callback(cb: PayCallback):
    rec = pay_store.get(cb.session_id)
    if not rec:
        raise HTTPException(404, "session unknown")
    pay_store.mark(cb.session_id, cb.status, cb.tx_id) # ???
    if cb.status == "success":
        draft: RegisterUser = draft_store.pop(cb.session_id)
        if draft:
            await register_user(draft, cb.tx_id)
    return Response(status_code=204)