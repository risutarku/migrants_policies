from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import engine, Base
from app.models.policy import Policy  # noqa: F401
from app.api import api_beorg_scan

from app.api import api_scan, api_payment, api_policy_file
from dotenv import load_dotenv
from pathlib import Path

# Так как uvicorn запускается из backend/src, .env лежит рядом:
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


description = {
    "title": "Policy issuer service",
    "version": "0.1.0",
    "description": "This service issues policies based on the provided data.",
}

app = FastAPI(**description, redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
     allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_scan.router, prefix="/scan")
app.include_router(api_payment.router, prefix="/payment", tags=["payment"])
app.include_router(api_policy_file.router, prefix="/policy", tags=["policy"])
app.include_router(api_beorg_scan.router, prefix="/scan", tags=["scan"])

Base.metadata.create_all(bind=engine)




