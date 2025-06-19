import pytest
import aiofiles
from datetime import datetime
from app.models.user import RegisterUser, SexEnum
from app.services.user_service import write_to_csv


@pytest.mark.asyncio
async def test_write_to_csv(tmp_path):
    csv_path = tmp_path / "test.csv"
    now = datetime.now()
    user = RegisterUser(
        name="Ivan",
        last_name="Petrov",
        middle_name="Sergeevich",
        sex=SexEnum.male,
        birthday=datetime(1990, 1, 1),
        passport_series=1234,
        passport_number=567890,
        passport_issue_date=datetime(2010, 1, 1),
        passport_expiry_date=None,
        passport_issuer="Passport Office",
        tx_id="TSX-123456789",
        create_date=now,
    )

    await write_to_csv(user, str(csv_path))
    async with aiofiles.open(csv_path, "r", encoding="utf-8") as f:
        content = await f.read()

    lines = content.strip().split("\n")

    assert (
        "name,last name,middle name,sex,birthday,passport series,passport number,passport issue date,passport expiry date,passport issuer,transaction id,create date"
        in lines[0]
    )
    assert (
        f"Ivan,Petrov,Sergeevich,male,01:01:1990,1234,567890,01:01:2010,None,Passport Office,TSX-123456789,{now.strftime('%d:%m:%Y %H:%M:%S')}"
        in lines[1]
    )
