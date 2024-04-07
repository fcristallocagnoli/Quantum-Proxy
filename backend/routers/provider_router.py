import json
from typing import Annotated

import requests
from bson import ObjectId
from pydantic import BaseModel, SkipValidation
from fastapi import APIRouter, HTTPException, Path, Body, Response, status
from utils.utils import get_current_time, norm_id
from database.schemas.provider_schema import provider_schema, providers_schema

from database.models.providers_models import BaseProvider
from database.mongo_client import (
    db_find_provider,
    db_find_providers,
    db_insert_provider,
    db_find_and_replace_provider,
    db_find_and_update_provider,
    db_find_and_delete_provider,
)


# For documentation purposes
class HTTPCodeModel(BaseModel):
    detail: str = None


router = APIRouter(prefix="/providers", tags=["Providers"])


@router.get(
    "",
    response_model=list[BaseProvider],
    response_model_exclude_none=True,
)
async def get_all_providers(
    filter: Annotated[
        dict, Body(title="Filter", description="Filter the providers")
    ] = {},
    projection: Annotated[
        dict, Body(title="Projection", description="Projection of the providers")
    ] = {},
) -> list[BaseProvider]:
    """
    Get all providers.
    - **filter**: Filter to query the providers.
    - **projection**: Filter to select which fields to return.
    - **returns**: All providers.
    """
    return providers_schema(db_find_providers(filter=filter, projection=projection))


@router.get(
    "/{id}",
    response_model=BaseProvider,
    response_model_exclude_none=True,
    responses={
        code: {"model": HTTPCodeModel}
        for code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
    },
)
async def get_specific_provider(
    id: Annotated[
        str,
        Path(
            title="The ID of the provider",
            # get the id of a provider to use as an example
            description="A 24-character alphanumeric string representing the provider's ID.",
            example=f"{norm_id(db_find_providers()[0])}",
        ),
    ],
    projection: Annotated[
        dict,
        Body(title="Projection", description="Projection of the provider", embed=True),
    ] = {},
) -> BaseProvider:
    """
    Get a especific provider.

    - **id**: The ID of the provider.
    - **returns**: The provider.
    - **raises**: HTTPException 400: If the ID format is incorrect.
    - **raises**: HTTPException 404: If the provider is not found.
    """
    try:
        object_id = ObjectId(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"El id {e}"
        )

    provider = db_find_provider(obj_id=ObjectId(object_id), projection=projection)

    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )

    return provider_schema(provider)


@router.post(
    "",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": BaseProvider},
        status.HTTP_409_CONFLICT: {"model": HTTPCodeModel},
    },
)
async def post_provider(provider: BaseProvider) -> Response:
    """
    Create a new provider.

    - **provider**: The provider to create.
    - **returns**: HTTP 201 Created: The provider created.
    - **raises**: HTTPException 409: If the provider already exists.
    """
    if db_find_provider(filter={"name": provider.name}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="El proveedor ya existe"
        )

    provider_dict = provider.model_dump(exclude="_id")

    provider_dict["last_checked"] = get_current_time()
    provider_dict["created_at"] = get_current_time()

    provider_db_id = db_insert_provider(provider_dict)
    provider_db = db_find_provider(filter=ObjectId(provider_db_id))

    return Response(
        status_code=status.HTTP_201_CREATED,
        media_type="application/json",
        content=json.dumps(provider_schema(provider_db)),
        headers={"Location": f"/providers/{provider_db_id}"},
    )


@router.delete(
    "/{id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "No Content"},
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
    },
)
async def delete_provider(
    id: Annotated[
        str,
        Path(
            title="The ID of the provider",
            # get the id of a provider to use as an example
            description="A 24-character alphanumeric string representing the provider's ID.",
            example=f"{norm_id(db_find_providers()[0])}",
        ),
    ],
):
    """
    Delete a specific provider.

    - **id**: The ID of the provider.
    - **returns**: HTTP 204 No Content
    - **raises**: HTTPException 404: If the provider is not found.
    """
    provider = db_find_and_delete_provider(filter={"_id": ObjectId(id)})
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="El proveedor no existe"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Mejor usar PATCH para actualizar solo los campos que se necesiten
@router.put(
    "/{id}",
    response_model=BaseProvider,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
    },
    tags=["Deprecated"],
    deprecated=True,
)
async def update_provider(
    id: Annotated[
        str,
        Path(
            title="The ID of the provider",
            # get the id of a provider to use as an example
            description="A 24-character alphanumeric string representing the provider's ID.",
            example=f"{norm_id(db_find_providers()[0])}",
        ),
    ],
    provider: BaseProvider,
) -> BaseProvider:
    """
    Replace a specific provider.

    - **id**: The ID of the provider.
    - **provider**: The provider's replacement.
    - **returns**: The previous provider.
    - **raises**: HTTPException 400: If the ID format is incorrect.
    - **raises**: HTTPException 404: If the provider is not found.
    """

    provider_dict = provider.model_dump(exclude="id")

    provider_dict["updated_at"] = get_current_time()
    doc_prev = db_find_and_replace_provider(
        filter={"_id": ObjectId(id)}, replacement=provider_dict
    )

    if not doc_prev:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )

    return BaseProvider(id=id, **doc_prev)


@router.patch(
    "/{id}",
    response_model=BaseProvider,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
    },
)
async def modify_provider(
    id: Annotated[
        str,
        Path(
            title="The ID of the provider",
            # get the id of a provider to use as an example
            description="A 24-character alphanumeric string representing the provider's ID.",
            example=f"{norm_id(db_find_providers()[0])}",
        ),
    ],
    provider: Annotated[BaseProvider, SkipValidation],
) -> BaseProvider:
    """
    Modify a specific provider.

    - **id**: The ID of the provider.
    - **provider**: The provider's modification.
    - **returns**: The previous provider.
    - **raises**: HTTPException 400: If the ID format is incorrect.
    - **raises**: HTTPException 404: If the provider is not found.
    """
    try:
        object_id = ObjectId(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"El id {e}"
        )
    prev = db_find_and_update_provider(
        filter={"_id": object_id},
        cambios={
            "$set": {
                **provider,
                # **user.model_dump(exclude_unset=True),
                "updated_at": get_current_time(),
            }
        },
    )
    if not prev:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
        )
    return BaseProvider(id=id, **prev)
