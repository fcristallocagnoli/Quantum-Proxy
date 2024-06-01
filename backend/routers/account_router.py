from typing import Annotated

from auth.utils import (
    basic_details,
    current_account,
    generate_jwt_token,
    generate_refresh_token,
    get_refresh_token,
    is_authenticated,
    is_authorized,
)
from utils.email_utils import send_verification_email
from utils.utils import (
    get_current_datetime,
    get_timestamp,
    hash_password,
    is_first_account,
    norm_id,
    sf_parse_object_id,
    verify_password,
)
from database.models.providers_models import BaseProviderModel
from database.models.user_models import UserInDBModel, UserModel
from fastapi import (
    Body,
    APIRouter,
    HTTPException,
    Path,
    Query,
    Request,
    Response,
    status,
)
from pydantic import BaseModel

from database.mongo_client import (
    db_delete_user,
    db_find_user,
    db_find_users,
    db_insert_user,
    db_update_user,
)

router = APIRouter(tags=["Accounts"])


class HTTPCodeModel(BaseModel):
    detail: str = None


@router.get(
    "/accounts",
    description="List all accounts",
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTPCodeModel}},
)
def get_accounts(request: Request) -> list[dict]:
    """
    List all of the account data in the database (from the frontend).
    """
    if not is_authenticated(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    users = list(map(lambda udb: UserInDBModel(**udb), db_find_users()))

    accounts = list(map(lambda u: basic_details(u), users))

    return accounts


@router.post(
    "/accounts",
    description="Add new account",
    response_model=UserInDBModel,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": BaseProviderModel},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_409_CONFLICT: {"model": HTTPCodeModel},
    },
)
def create_account(request: Request, user: dict = Body(...)) -> UserInDBModel:
    """
    Insert a new account (from the frontend).
    """
    if not is_authenticated(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    if db_find_user(filter={"email": user["email"]}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user["email"]} is already registered",
        )

    user_to_store = {
        "first_name": user["firstName"],
        "last_name": user["lastName"],
        "email": user["email"],
        "password": hash_password(user["password"]),
        "roles": [user["role"]],
        "is_verified": True,
        "created_at": get_current_datetime(),
    }

    new_user_id = db_insert_user(user_to_store)
    created_user = db_find_user(filter=sf_parse_object_id(new_user_id))

    return created_user


@router.post(
    "/accounts/register",
    description="Register new account",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInDBModel,
    responses={
        status.HTTP_201_CREATED: {"model": BaseProviderModel},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_409_CONFLICT: {"model": HTTPCodeModel},
    },
)
def register_account(user: UserModel = Body(...)) -> UserInDBModel:
    """
    Register new account (from the frontend).
    """
    if not (user.email and user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password fields are required",
        )
    if db_find_user(filter={"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"""
                <h4>Email Already Registered</h4>
                <p>The email {user.email} is already registered.</p>
                """,
        )

    # user.username = user.first_name[0].lower() + user.last_name.split(" ")[0].lower()
    user.roles = ["Admin"] if is_first_account() else ["User"]
    user.password = hash_password(user.password)
    user.created_at = get_current_datetime()

    user = UserInDBModel(
        **user.model_dump(),
        verification_token=get_timestamp(),
        is_verified=True if is_first_account() else False,
        refresh_tokens=[],
    )

    new_user_id = db_insert_user(user.model_dump(by_alias=True, exclude=["id"]))
    created_user = db_find_user(filter=sf_parse_object_id(new_user_id))

    # Send verification email
    send_verification_email(
        user.email,
        f"http://localhost:4200/account/verify-email?token={user.verification_token}",
    )

    return created_user


@router.get(
    "/accounts/verify-email",
    description="Verify email",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
    },
)
def verify_email(token: Annotated[str, Query(...)]):
    """
    Verify email (from the frontend).
    """
    user = db_update_user(
        filter={"verification_token": float(token)}, cambios={"$set": {"is_verified": True}}
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification failed",
        )


@router.post(
    "/accounts/authenticate",
    description="Authenticate account",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    responses={
        status.HTTP_201_CREATED: {"model": BaseProviderModel},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
    },
)
def authenticate_account(
    response: Response, email: str = Body(...), password: str = Body(...)
) -> dict:
    """
    Authenticate account (from the frontend).
    """
    # Account must match email and password, and be verified
    filter = {"email": email, "is_verified": True}

    if not (user := db_find_user(filter=filter)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password is incorrect",
        )

    if not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password is incorrect",
        )

    cambios = {"$push": {"refresh_tokens": generate_refresh_token(response)}}

    if not (user := db_update_user(filter=filter, cambios=cambios)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or password is incorrect",
        )

    user = UserInDBModel(**user)

    account = basic_details(user)
    account.update({"jwtToken": generate_jwt_token(user)})

    return account


@router.post(
    "/accounts/revoke-token",
    description="Revoke token",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPCodeModel},
    },
)
def revoke_token(
    request: Request,
):
    """
    Revoke token (from the frontend).
    """
    if not is_authenticated(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    refresh_token = get_refresh_token(request)

    filter = {"refresh_tokens": refresh_token}
    cambios = {"$pull": {"refresh_tokens": refresh_token}}

    db_update_user(filter=filter, cambios=cambios)


@router.post(
    "/accounts/refresh-token",
    description="Refresh token",
    response_model=dict,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPCodeModel},
    },
)
def refresh_token(
    request: Request,
    response: Response,
) -> dict:
    """
    Refresh token (from the frontend).
    """
    if not (refresh_token := get_refresh_token(request)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    filter = {"refresh_tokens": refresh_token}

    if not (account := db_find_user(filter=filter)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    refresh_token_list = list(account["refresh_tokens"])
    refresh_token_list.remove(refresh_token)
    refresh_token_list.append(generate_refresh_token(response))

    cambios = {"$set": {"refresh_tokens": refresh_token_list}}

    user = UserInDBModel(**db_update_user(filter=filter, cambios=cambios))

    account = basic_details(user)
    account.update({"jwtToken": generate_jwt_token(user)})

    return account


@router.get(
    "/accounts/{id}",
    description="Get a single account (from the frontend).",
    response_model=dict,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPCodeModel},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
    },
)
def get_account(
    request: Request,
    id: Annotated[
        str,
        Path(
            title="The ID of the account",
            # get the id of a account to use as an example
            description="A 24-character alphanumeric string representing the account's ID.",
            example=f"{norm_id(db_find_users()[0])}",
        ),
    ],
) -> dict:

    if not is_authenticated(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    user_to_query = UserInDBModel(**db_find_user(filter=sf_parse_object_id(id)))

    if not user_to_query:
        raise HTTPException(status_code=404, detail=f"Account with {id} not found")

    account = current_account(request)

    # user accounts can get OWN profile
    # admin accounts can get ALL profiles
    if not account or (
        user_to_query.id != account.id and not is_authorized(account, "Admin")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    return basic_details(user_to_query)


@router.put(
    "/accounts/{id}",
    description="Update an account (from the frontend).",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPCodeModel},
    },
)
def update_account(
    request: Request,
    id: Annotated[
        str,
        Path(
            title="The ID of the account",
        ),
    ],
    new_user: dict = Body(...),
):

    if not is_authenticated(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    user_to_update = UserInDBModel(**db_find_user(filter=sf_parse_object_id(id)))

    account = current_account(request)

    # user accounts can update OWN profile
    # admin accounts can update ALL profiles
    if not account or (
        user_to_update.id != account.id and not is_authorized(account, "Admin")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    user_to_store = {
        "first_name": new_user["firstName"],
        "last_name": new_user["lastName"],
        "email": new_user["email"],
    }
    
    # Only change password if it is not empty
    if password := new_user["password"]:
        user_to_store["password"] = hash_password(password)

    # Only admins can change roles
    if "role" in new_user:
        user_to_store["roles"] = [new_user["role"]]

    user_in_db = db_update_user(
        filter={"_id": sf_parse_object_id(id)}, cambios={"$set": user_to_store}
    )

    return {
        "id": str(user_in_db["_id"]),
        "firstName": user_in_db["first_name"],
        "lastName": user_in_db["last_name"],
        "email": user_in_db["email"],
        "role": user_in_db["roles"][0],
    }


@router.delete(
    "/accounts/{id}",
    description="Delete an aacount",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "No content"},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
    },
)
def delete_account(
    request: Request,
    id: Annotated[
        str,
        Path(
            title="The ID of the account",
            # get the id of a account to use as an example
            description="A 24-character alphanumeric string representing the account's ID.",
            example=f"{norm_id(db_find_users()[0])}",
        ),
    ],
):
    """
    Remove a single account (from the frontend).
    """

    if not is_authenticated(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    user_to_delete = UserInDBModel(**db_find_user(filter=sf_parse_object_id(id)))

    account = current_account(request)

    # user accounts can delete OWN account
    # admin accounts can delete ANY account
    if not account or (
        user_to_delete.id != account.id and not is_authorized(account, "Admin")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    if db_delete_user(filter={"_id": sf_parse_object_id(id)}):
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Account with {id} not found")