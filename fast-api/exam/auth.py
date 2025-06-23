from fastapi import Header, HTTPException, status
from typing import Optional


CREDENTIALS = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine",
    "admin": "4dm1N"
}

def basic_auth(
    authorization: Optional[str] = Header(None, alias = "Authorization")
):
    if not authorization or not authorization.startswith("Basic "):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Missing or malformed `Authorization` header"
        )
    user, pw = authorization[len("Basic "):].split(":", 1)
    if CREDENTIALS.get(user) != pw:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Bad credentials"
        )
    return user
