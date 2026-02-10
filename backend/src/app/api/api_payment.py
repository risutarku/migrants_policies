from fastapi import APIRouter, HTTPException, Depends
import httpx
from uuid import UUID
import asyncio, time, random
from sqlalchemy.orm import Session

from app.models.payment import (
    PolicyDraftSaveReq,
    PolicyDraftSaveResp,
    PayInitReq,
    PayInitResp,
    PayStatusResp,
    PayCallback,
)
from app.services.payment_service import pay_store
from app.services.policy_db_service import create_policy_draft, mark_policy_paid
from app.models.to_csv import RegisterUser
from app.db import get_db

router = APIRouter()


@router.post("/draft-save", response_model=PolicyDraftSaveResp, status_code=201)
async def save_policy_draft(p: PolicyDraftSaveReq, db: Session = Depends(get_db)):
    """
    Сохраняет черновик полиса в БД.
    Вызывается с фронта на кнопке 'К оплате'.
    """
    draft = RegisterUser(user=p.user, contacts=p.contacts, policy=p.policy)
    policy_id = await create_policy_draft(
        draft=draft,
        employee_tab_number=p.employee_tab_number,
        arrived_for_hire=p.arrived_for_hire,
        lang=p.lang,
        policy_variant=p.policy_variant,
        db=db,
    )

    # Запоминаем amount на бэке, чтобы /payment/init мог взять сумму без доп. запроса в БД
    pay_store.remember_policy_amount(policy_id, p.policy.amount)

    return PolicyDraftSaveResp(policy_id=policy_id)


@router.post("/init", response_model=PayInitResp, status_code=201)
async def payment_init(req: PayInitReq, db: Session = Depends(get_db)):
    """
    Инициирует оплату для существующего policy_id.
    """

    # 1) Берём amount из памяти (обычный сценарий: draft-save уже был)
    amount = pay_store.get_policy_amount(req.policy_id)

    # 2) Fallback: если сервер перезапускали и память очистилась
    if amount is None:
        amount = await pay_store.get_amount_for_policy(req.policy_id, db)
        if amount <= 0:
            raise HTTPException(404, "policy not found or amount missing")
        pay_store.remember_policy_amount(req.policy_id, amount)

    sid = pay_store.create(req.session_id, req.idempotency_key, amount)
    pay_store.attach_policy(sid, req.policy_id)

    if pay_store.get(sid)["status"] == "pending":
        asyncio.create_task(_mock_terminal(sid))

    return PayInitResp(session_id=sid, amount=amount)


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
    return PayStatusResp(
        session_id=sid,
        status=rec["status"],
        tx_id=rec.get("tx_id"),
    )


@router.post("/callback", status_code=204)
async def payment_callback(cb: PayCallback, db: Session = Depends(get_db)):
    """
    Callback после успешной оплаты.
    Обновляет статус полиса в БД.
    """
    rec = pay_store.get(cb.session_id)
    if not rec:
        raise HTTPException(404, "session unknown")

    pay_store.mark(cb.session_id, cb.status, cb.tx_id)

    if cb.status == "success":
        policy_id = rec.get("policy_id")
        if policy_id:
            await mark_policy_paid(policy_id, cb.tx_id, db)

    return None
