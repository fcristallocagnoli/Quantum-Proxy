import base64
import json

from database.models.user_models import UserInDBModel
from database.mongo_client import db_find_user
from fastapi import Request, Response
from utils.utils import get_timestamp, sf_parse_object_id


def generate_refresh_token(response: Response):
    token = get_timestamp()

    # add token cookie that expires in 7 days
    from datetime import datetime, timedelta, timezone

    future_date = datetime.now(timezone.utc) + timedelta(days=7)
    utc_string = future_date.strftime("%a, %d %b %Y %H:%M:%S GMT")

    response.set_cookie(
        key="refreshToken",
        value=token,
        expires=utc_string,
        path="/",
    )

    return token


def generate_jwt_token(account: UserInDBModel):
    from datetime import datetime, timedelta, timezone

    future_time = datetime.now(timezone.utc) + timedelta(minutes=15)
    expires = round(future_time.timestamp())
    # create token that expires in 15 minutes
    token_payload = {"exp": expires, "id": account.id}
    payload_json = json.dumps(token_payload)
    payload_base64 = base64.b64encode(payload_json.encode()).decode()

    return f"jwt-token.{payload_base64}"


def is_authenticated(request):
    return current_account(request) is not None


def current_account(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header and not auth_header.startswith("Bearer jwt-token"):
        return None

    token_fragment = auth_header.split(".")[1]
    jwt_token = json.loads(base64.b64decode(token_fragment).decode())

    is_expired = get_timestamp() > (jwt_token["exp"] * 1000)
    if is_expired:
        return None

    user = db_find_user(filter={"_id": sf_parse_object_id(jwt_token["id"])})

    return user


def get_refresh_token(request: Request):
    # get refresh token from cookie
    cookies = request.cookies
    return float(cookies.get("refreshToken"))
