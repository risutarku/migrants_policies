from fastapi import FastAPI
from app.api import api_insurance, api_user, api_scan, api_payment, api_policy_file
from fastapi.middleware.cors import CORSMiddleware

description = {
    "title": "Policy issuer service",
    "version": "0.1.0",
    "description": "This service issues policies based on the provided data.",
}


app = FastAPI(**description)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_user.router, prefix="/user", tags=["user"])
app.include_router(api_insurance.router, prefix="/insurance", tags=["insurance"])
app.include_router(api_scan.router, prefix="/scan")
app.include_router(api_payment.router, prefix="/payment", tags=["payment"])
app.include_router(api_policy_file.router, prefix="/policy", tags=["policy"])