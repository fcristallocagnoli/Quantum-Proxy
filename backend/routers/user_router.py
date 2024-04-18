from datetime import datetime
from typing import Annotated

from bson import ObjectId
from utils.utils import norm_id
from database.models.providers_models import BaseProviderModel
from database.models.user_models import UserDTO, UserModel, UpdateUserModel
from fastapi import Body, APIRouter, HTTPException, Path, Response, status
from pydantic import BaseModel

from database.mongo_client import (
    db_delete_user,
    db_find_user,
    db_find_users,
    db_insert_user,
    db_update_user,
)

router = APIRouter(tags=["Users"])


class HTTPCodeModel(BaseModel):
    detail: str = None


@router.get(
    "/users/",
    description="List all users",
    response_model=list[UserDTO],
    response_model_by_alias=False,
    # Para en caso de usar projection, no devolver campos nulos
    response_model_exclude_none=True,
)
def get_users(
    filter: Annotated[dict, Body(title="Filter", description="Filter the users")] = {},
    projection: Annotated[
        dict, Body(title="Projection", description="Project the users")
    ] = {},
) -> list[UserDTO]:
    """
    List all of the user data in the database.
    """
    return db_find_users(filter=filter, projection=projection)


@router.get(
    "/users/{id}",
    description="Get a single user",
    response_model=UserDTO,
    response_model_by_alias=False,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
    },
    # Para en caso de usar projection, no devolver campos nulos
    response_model_exclude_none=True,
)
def get_user(
    id: Annotated[
        str,
        Path(
            title="The ID of the user",
            # get the id of a user to use as an example
            description="A 24-character alphanumeric string representing the user's ID.",
            example=f"{norm_id(db_find_users()[0])}",
        ),
    ],
    projection: Annotated[
        dict, Body(title="Projection", description="Project the users", embed=True)
    ] = {},
) -> UserDTO:

    object_id = sf_parse_object_id(id)

    if (user := db_find_user(filter=object_id, projection=projection)) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.post(
    "/users/",
    description="Add new user",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    responses={
        status.HTTP_201_CREATED: {"model": BaseProviderModel},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_409_CONFLICT: {"model": HTTPCodeModel},
    },
)
def post_user(user: UserModel = Body(...)) -> UserModel:
    """
    Insert a new user record.

    A unique `id` will be created and provided in the response.
    """
    if (db_find_user(filter={"email": user.email})) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                f"User with email {user.email} already exists",
                "Email field must be unique",
            ],
        )

    user.created_at = datetime.now()

    new_user_id = db_insert_user(user.model_dump(by_alias=True, exclude=["id"]))
    created_user = db_find_user(filter=sf_parse_object_id(new_user_id))

    return created_user


@router.patch(
    "/users/{id}",
    description="Update a user",
    response_model=UserModel,
    response_model_by_alias=False,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
        status.HTTP_409_CONFLICT: {"model": HTTPCodeModel},
    },
)
def update_user(
    id: Annotated[
        str,
        Path(
            title="The ID of the user",
            # get the id of a user to use as an example
            description="A 24-character alphanumeric string representing the user's ID.",
            example=f"{norm_id(db_find_users()[0])}",
        ),
    ],
    user: UpdateUserModel = Body(...),
) -> UserModel:
    """
    Update individual fields of an existing user record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    user: dict = {
        k: v for k, v in user.model_dump(by_alias=True).items() if v is not None
    }

    user.pop("_id", None)
    if "email" in user:
        if (existing_user := db_find_user(filter={"email": user["email"]})) is not None:
            if existing_user.get("_id") != sf_parse_object_id(id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=[
                        f"User with email {user['email']} already exists",
                        "Email field must be unique",
                    ],
                )

    if len(user) >= 1:
        api_keys: dict = user.pop("api_keys", None)

        if api_keys is not None:
            user.update({f"api_keys.{k}": v for k, v in api_keys.items()})

        update_result = db_update_user(
            filter={"_id": sf_parse_object_id(id)},
            cambios={"$set": user},
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"User {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_user := db_find_user(filter=sf_parse_object_id(id))) is not None:
        return existing_user

    raise HTTPException(status_code=404, detail=f"User {id} not found")


@router.delete(
    "/users/{id}",
    description="Delete a user",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "No content"},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
    },
)
def delete_user(
    id: Annotated[
        str,
        Path(
            title="The ID of the user",
            # get the id of a user to use as an example
            description="A 24-character alphanumeric string representing the user's ID.",
            example=f"{norm_id(db_find_users()[0])}",
        ),
    ],
):
    """
    Remove a single user record from the database.
    """

    if db_delete_user(filter={"_id": sf_parse_object_id(id)}):
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"User {id} not found")


def sf_parse_object_id(id: str) -> ObjectId:
    """
    Safe parse from str to ObjectId.
    :raises HTTPException 400: if the id is not valid
    """
    try:
        object_id = ObjectId(id)
        return object_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id {e}"
        )
