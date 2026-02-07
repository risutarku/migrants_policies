from fastapi import APIRouter
from app.models.scan import ScanResponse
import asyncio

router = APIRouter(tags=["scan"])


@router.post("/", response_model=ScanResponse)
async def scan():
    """
    Endpoint to trigger a scan operation.
    This is a placeholder for the actual scan logic.
    """
    await asyncio.sleep(2)
    # Here you would implement the logic for scanning, e.g., scanning files, directories, etc.
    return {
        "first_name":         "Ivan",
        "last_name":          "Ivanov",
        "middle_name":        "Ivanovich",
        "sex":                "male",
        "birthday":           "1990-01-01",
        "passport_series":    1234,
        "passport_number":    567890,
        "passport_issue_date": "2015-01-01",
        "passport_expiry_date": None,
        "passport_issuer":    "OVD Moscow",
    }