from __future__ import annotations

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.beorg_api_service import BeorgConfig, scan_passport, BeorgApiError

router = APIRouter()


class BeorgScanReq(BaseModel):
    images: list[str]
    with_registration: bool = True


@router.post("/beorg-passport")
async def beorg_scan(req: BeorgScanReq):
    cfg = BeorgConfig(
        base_url=os.getenv("BEOCR_BASE_URL", "").strip(),
        token=os.getenv("BEOCR_TOKEN", "").strip(),
        machine_uid=os.getenv("BEOCR_MACHINE_UID", "").strip(),
        project_id=os.getenv("BEOCR_PROJECT_ID", "").strip(),
    )
    if not (cfg.base_url and cfg.token and cfg.machine_uid and cfg.project_id):
        raise HTTPException(500, "Beorg API config missing (BEOCR_BASE_URL/TOKEN/MACHINE_UID/PROJECT_ID)")

    try:
        return await scan_passport(cfg, req.images, with_registration=req.with_registration)
    except BeorgApiError as e:
        # 502 = внешний сервис упал/ответил ошибкой
        raise HTTPException(502, str(e))
