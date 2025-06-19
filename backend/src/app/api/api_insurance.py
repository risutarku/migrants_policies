from fastapi import routing

router = routing.APIRouter()
from app.langs.policy import ISURRANSE
from pydantic import BaseModel


class LangRequest(BaseModel):
    lang: str

@router.post("/")
async def get_insurance_info(request: LangRequest):
    lang = request.lang or "ru"
    return ISURRANSE.get(lang, ISURRANSE["ru"])
