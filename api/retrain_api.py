from fastapi import APIRouter, Header, HTTPException
from jose import jwt
import subprocess
import os

router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGO = "HS256"

def verify_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/retrain")
def retrain_model(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token missing")

    token = authorization.split(" ")[1]

    verify_token(token)

    subprocess.Popen(
        ["python", "model/train_model.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return {"status": "retraining started"}
