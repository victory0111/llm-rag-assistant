from datetime import datetime
from datetime import timedelta

import jwt

from app.config.settings import settings

def create_access_token(
        data: dict
):

    payload = data.copy()

    expire = (
        datetime.utcnow()
        + timedelta(
            minutes=settings.jwt_expire_minutes
        )
    )

    payload["exp"] = expire

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

    return token

def verify_token(
        token: str
):

    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[
            settings.jwt_algorithm
        ]
    )