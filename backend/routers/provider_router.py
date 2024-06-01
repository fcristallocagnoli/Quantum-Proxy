from typing import Annotated

from bson import ObjectId
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Path, Body, Response, status
from utils.utils import get_current_time_iso, norm_str

from database.models.providers_models import (
    BaseProviderModel,
)
from database.mongo_client import (
    db_find_provider,
    db_find_providers,
    db_insert_provider,
    db_replace_provider,
    db_update_provider,
    db_delete_provider,
)


# For documentation purposes
class HTTPCodeModel(BaseModel):
    detail: str = None


router = APIRouter(tags=["Providers"], prefix="/providers")


@router.get(
    "",
    description="List all providers",
    response_model=list[BaseProviderModel],
    response_model_by_alias=False,
    # Para en caso de usar projection, no devolver campos nulo
    response_model_exclude_none=True,
)
async def get_providers() -> list[BaseProviderModel]:
    """
    Get all providers.
    - **returns**: All providers.
    """
    return db_find_providers()

@router.post(
    "",
    description="List providers (filtered and/or projected)",
    response_model=list[BaseProviderModel],
    response_model_by_alias=False,
    # Para en caso de usar projection, no devolver campos nulo
    response_model_exclude_none=True,
)
async def get_providers_filtered(
    filter: Annotated[
        dict, Body(title="Filter", description="Filter the providers")
    ] = {},
    projection: Annotated[
        dict, Body(title="Projection", description="Project the providers")
    ] = {},
) -> list[BaseProviderModel]:
    """
    Get providers (filtered and/or projected).
    - **filter**: Filter to query the providers.
    - **projection**: Filter to select which fields to return.
    - **returns**: All providers.
    """
    return db_find_providers(filter=filter, projection=projection)


@router.get(
    "/{pid}",
    description="Get a single provider",
    response_model=BaseProviderModel,
    response_model_by_alias=False,
    responses={
        code: {"model": HTTPCodeModel}
        for code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
    },
    # Para en caso de usar projection, no devolver campos nulos
    response_model_exclude_none=True,
)
async def get_provider(
    pid: Annotated[
        str,
        Path(
            title="The PID (Provider Identifier)",
        ),
    ],
    projection: Annotated[
        dict,
        Body(title="Projection", description="Projection of the provider", embed=True),
    ] = {},
) -> BaseProviderModel:
    """
    Get a single provider.

    - **pid**: The PID (Provider Identifier).
    - **returns**: The provider.
    - **raises**: HTTPException 400: If the PID does not exist.
    - **raises**: HTTPException 404: If the provider is not found.
    """

    if (
        provider := db_find_provider(filter={"pid": pid}, projection=projection)
    ) is not None:
        return provider

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Provider with {pid} not found"
    )


@router.post(
    "",
    description="Add new provider",
    response_model=BaseProviderModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    responses={
        status.HTTP_201_CREATED: {"model": BaseProviderModel},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_409_CONFLICT: {"model": HTTPCodeModel},
    },
)
async def post_provider(provider: BaseProviderModel = Body(...)) -> BaseProviderModel:
    """
    Insert a new provider record.

    - **provider**: The provider to create.
    - **returns**: HTTP 201 Created: The provider created.
    - **raises**: HTTPException 409: If the provider already exists.
    """
    # Generamos el pid del proveedor
    if not provider.pid:
        provider_name = norm_str(provider.name)
        if provider.third_party:
            provider.pid = ".".join([norm_str(provider.third_party), provider_name])
        else:
            provider.pid = ".".join(["native", provider_name])
    if db_find_provider(filter={"pid": provider.pid}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="El proveedor ya existe"
        )

    provider_dict = provider.model_dump(by_alias=True, exclude="_id")

    provider_dict["last_updated_at"] = get_current_time_iso()

    provider_db_id = db_insert_provider(provider_dict)
    provider_db = db_find_provider(filter=sf_parse_object_id(provider_db_id))

    return provider_db


# Mejor usar PATCH para actualizar solo los campos que se necesiten
@router.put(
    "/{pid}",
    response_model=BaseProviderModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
    },
    tags=["Deprecated"],
    deprecated=True,
)
async def update_provider(
    pid: Annotated[
        str,
        Path(
            title="The PID (Provider Identifier)",
        ),
    ],
    provider: BaseProviderModel,
) -> BaseProviderModel:
    """
    Replace a specific provider.

    - **pid**: The PID (Provider Identifier).
    - **provider**: The provider's replacement.
    - **returns**: The previous provider.
    - **raises**: HTTPException 400: If the PID does not exist.
    - **raises**: HTTPException 404: If the provider is not found.
    """

    provider_dict = provider.model_dump(exclude=["id"])

    provider_dict["last_updated_at"] = get_current_time_iso()
    doc_after = db_replace_provider(filter={"pid": pid}, replacement=provider_dict)

    if not doc_after:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Provider with {pid} not found",
        )

    return doc_after


@router.patch(
    "/{pid}",
    description="Modify a provider",
    response_model=BaseProviderModel,
    response_model_by_alias=False,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
        status.HTTP_409_CONFLICT: {"model": HTTPCodeModel},
    },
)
async def modify_provider(
    pid: Annotated[
        str,
        Path(
            title="The PID (Provider Identifier)",
        ),
    ],
    provider: BaseProviderModel,
) -> BaseProviderModel:
    """
    Modify a specific provider.

    - **pid**: The PID (Provider Identifier).
    - **provider**: The provider's modification.
    - **returns**: The previous provider.
    - **raises**: HTTPException 400: If the PID does not exist.
    - **raises**: HTTPException 404: If the provider is not found.
    """
    provider: dict = {
        k: v for k, v in provider.model_dump(by_alias=True).items() if v is not None
    }

    provider.pop("_id", None)

    if len(provider) >= 1:
        update_result = db_update_provider(
            filter={"pid": pid},
            cambios={"$set": provider},
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(
                status_code=404, detail=f"Provider with {pid} not found"
            )


@router.delete(
    "/{pid}",
    description="Delete a provider",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "No Content"},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
    },
)
async def delete_provider(
    pid: Annotated[
        str,
        Path(
            title="The PID (Provider Identifier)",
        ),
    ],
):
    """
    Delete a single provider record from the database.

    - **pid**: The PID (Provider Identifier)
    - **returns**: HTTP 204 No Content
    - **raises**: HTTPException 404: If the provider is not found.
    """
    if db_delete_provider(filter={"pid": pid}):
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Provider with {pid} not found")


# region Utils ----------------------------


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
