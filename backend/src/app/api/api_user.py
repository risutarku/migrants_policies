from fastapi import routing, status
from fastapi.responses import Response
from app.models.to_csv import RegisterUser
from app.services.user_service import record_user_data_service


router = routing.APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: RegisterUser):
    try:
        await record_user_data_service(user_data)
    except Exception as e:
        print(f"Error processing user registration: {e}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return {
        "payment_id": "TX-123"
    }