from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List

import httpx


@dataclass
class BeorgConfig:
    base_url: str            # например: "http://155.212.182.196:81"
    token: str
    machine_uid: str
    project_id: str


class BeorgApiError(RuntimeError):
    pass


def _extract_fields(result: Dict[str, Any]) -> Dict[str, Any]:
    docs = result.get("documents") or []
    if not docs:
        return {}
    data = (docs[0] or {}).get("data") or {}

    return {
        "last_name": data.get("LastName") or "",
        "first_name": data.get("FirstName") or "",
        "middle_name": data.get("MiddleName") or "",
        "sex": data.get("Gender") or "",
        "birthday": data.get("BirthDate") or "",
        "passport_series": data.get("Series") or "",
        "passport_number": data.get("Number") or "",
        "passport_issuer": data.get("IssuedBy") or "",
        "passport_issue_date": data.get("IssueDate") or "",
        "passport_issue_id": data.get("IssueId") or "",
        "birth_place": data.get("BirthPlace") or "",
    }


async def add_document(cfg: BeorgConfig, images_b64: List[str], doc_type: str) -> str:
    url = f"{cfg.base_url.rstrip('/')}/api/bescan/add_document"

    # как в примере с сайта: process_info на каждую картинку
    process_info = [{"type": doc_type, "key": doc_type} for _ in images_b64]

    payload = {
        "token": cfg.token,
        "project_id": cfg.project_id,
        "machine_uid": cfg.machine_uid,
        "images": images_b64,
        "process_info": process_info,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, json=payload, headers={"Content-Type": "application/json"})

        # Для диагностики:
        if r.status_code != 200:
            raise BeorgApiError(f"add_document failed: HTTP {r.status_code} {r.text}")

        data = r.json()
        doc_id = data.get("document_id")
        if not doc_id:
            raise BeorgApiError(f"add_document: no document_id in response: {data}")
        return str(doc_id)


async def get_result(cfg: BeorgConfig, document_id: str) -> Dict[str, Any]:
    # ВАЖНО: token в query string как в примере
    url = f"{cfg.base_url.rstrip('/')}/api/document/result/{document_id}"

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(url, params={"token": cfg.token})

        if r.status_code == 200:
            out = r.json()
            out["_status"] = "ready"
            return out

        # 425/202/и т.п. — документ ещё обрабатывается, но сервис может отдавать и другие коды
        return {"_status": "processing", "_code": r.status_code, "_body": r.text}


async def scan_passport(
    cfg: BeorgConfig,
    images_b64: List[str],
    with_registration: bool,
    is_russian_passport: bool = True,
) -> Dict[str, Any]:
    doc_type = "PASSPORT" if is_russian_passport else "PASSPORT_FRGN"

    doc_id = await add_document(cfg, images_b64, doc_type=doc_type)

    deadline = asyncio.get_event_loop().time() + 120.0
    while True:
        res = await get_result(cfg, doc_id)

        if res.get("_status") == "ready":
            return {"document_id": doc_id, "fields": _extract_fields(res)}

        if asyncio.get_event_loop().time() >= deadline:
            # покажем последнюю “ошибку/ответ”
            raise BeorgApiError(f"timeout waiting result, last={res.get('_code')} {res.get('_body')}")

        await asyncio.sleep(1.0)
