import secrets
from api.hello import router
from fastapi import APIRouter, Depends, Header, HTTPException, status

from app.core.config import API_AUTH_TOKEN


class AuthRoute(APIRouter):
    def __init__(self, **kwargs):
        kwargs["dependencies"] = [Depends(verify_bearer_token)]
        super().__init__(**kwargs)


async def verify_bearer_token(Authorization: str = Header(...)):
    if not (secrets.compare_digest(Authorization, f"Bearer {API_AUTH_TOKEN}")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer Token header invalid",
        )
