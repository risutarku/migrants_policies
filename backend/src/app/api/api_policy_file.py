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


# @router.post("/quote")
# def quote(req: QuoteReq):
#     c = compute_policy(
#         employee_tab_number=req.inputs.employee_tab_number,
#         arrived_for_hire=req.inputs.arrived_for_hire,
#         last_name=req.user.last_name,
#         first_name=req.user.first_name,
#         middle_name=req.user.middle_name,
#         birthday=req.user.birthday,
#         passport_series=req.user.passport_series,
#         passport_number=req.user.passport_number,
#         start_date=req.inputs.start_date,
#         end_date=req.inputs.end_date,
#         base_premium=req.inputs.base_premium,
#         seq=req.inputs.seq,
#     )

#     return {
#         "policy_number": c.policy_number,
#         "issue_date": c.issue_date,
#         "arrival_purpose": c.arrival_purpose,
#         "start_date": c.start_date,
#         "end_date": c.end_date,
#         "insurance_days": c.insurance_days,
#         "insured_full_name": c.insured_full_name,
#         "birthday": c.birthday,
#         "document_number": c.document_number,
#         "premium_total": c.premium_total,
#     }


# class QuoteOut(BaseModel):
#     policy_number: str
#     issue_date: date
#     arrival_purpose: str
#     start_date: date
#     end_date: date
#     insurance_days: int
#     insured_full_name: str
#     birthday: date
#     document_number: str
#     premium_total: float


# @router.post("/generate-xlsx-from-quote")
# def generate_xlsx_from_quote(q: QuoteOut):
#     values = {
#         "policy_number": q.policy_number,
#         "issue_date": q.issue_date,
#         "start_date": q.start_date,
#         "end_date": q.end_date,
#         "insurance_days": q.insurance_days,
#         "insured_full_name": q.insured_full_name,
#         "birthday": q.birthday,
#         "document_number": q.document_number,
#         "premium_total": q.premium_total,
#     }
#     out_path = render_policy_xlsx(values, out_name=q.policy_number)
#     return FileResponse(
#         path=str(out_path),
#         filename=out_path.name,
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#     )


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