from __future__ import annotations

from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.policy_calc_service import compute_policy
from app.services.policy_file_service import render_policy_xlsx
from app.services.policy_db_service import get_policy_for_xlsx
from app.db import get_db


router = APIRouter()


class QuoteInputs(BaseModel):
    employee_tab_number: str
    arrived_for_hire: bool = False
    start_date: date | None = None
    end_date: date | None = None
    base_premium: float = 1000.0
    seq: int = 1  # пока временно


class UserIn(BaseModel):
    last_name: str
    first_name: str
    middle_name: str | None = None
    birthday: date
    passport_series: str
    passport_number: str


class QuoteReq(BaseModel):
    user: UserIn
    inputs: QuoteInputs

@router.get("/download/{policy_id}")
async def download_policy(policy_id: int, db: Session = Depends(get_db)):
    values = await get_policy_for_xlsx(policy_id, db)
    if not values:
        raise HTTPException(404, "Policy not found or not paid")

    out_path = render_policy_xlsx(values, out_name=values["policy_number"])
    return FileResponse(
        path=str(out_path),
        filename=out_path.name,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )