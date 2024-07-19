from typing import Annotated

from utils.scheduler_functions import refresh_backends
from database.models.backends_models import Backend, retrieve_backend
from database.mongo_client import (
    db_find_backend,
    db_find_backends,
    db_find_provider,
    db_find_providers,
)
from fastapi import APIRouter, Body, HTTPException, Path, status
from fastapi.logger import logger
from pydantic import BaseModel
from routers.provider_router import sf_parse_object_id

from database.models.providers_models import BaseProviderModel, ThirdPartyEnum


# For documentation purposes
class HTTPCodeModel(BaseModel):
    detail: str = None


router = APIRouter(tags=["Systems"], prefix="/backends")


@router.get(
    "",
    description="List all backends",
    response_model=list[dict],
    response_model_by_alias=False,
    # Para en caso de usar projection, no devolver campos nulo
    response_model_exclude_none=True,
)
async def get_backends() -> list[dict]:
    """
    Get all backends.
    - **returns**: All backends.
    """
    backends = list(
        map(
            lambda b: retrieve_backend(Backend(backend=b), as_dict=True),
            db_find_backends(),
        )
    )
    return backends


@router.post(
    "",
    description="List backends (filtered and/or projected)",
    response_model=list[dict],
    response_model_by_alias=False,
    # Para en caso de usar projection, no devolver campos nulo
    response_model_exclude_none=True,
)
async def get_backends_filtered(
    usingObjectId: Annotated[
        dict,
        Body(title="Using ObjectID", description="Whether is requesting ObjectId or not"),
    ] = None,
    filter: Annotated[
        dict, Body(title="Filter", description="Filter the backends")
    ] = {},
    projection: Annotated[
        dict, Body(title="Projection", description="Project the backends")
    ] = {},
) -> list[dict]:
    """
    Get backends (filtered and/or projected).
    - **filter**: Filter to query the backends.
    - **projection**: Filter to select which fields to return.
    - **returns**: All backends.
    """
    if usingObjectId and usingObjectId.get("usingObjectId"):
        for key, value in filter.items():
            filter[key] = sf_parse_object_id(value)
    backends = list(
        map(
            lambda b: retrieve_backend(Backend(backend=b), as_dict=True),
            db_find_backends(filter=filter, projection=projection),
        )
    )
    return backends


@router.get(
    "/{bid}",
    description="Get a single backend",
    response_model=dict,
    response_model_by_alias=False,
    responses={
        code: {"model": HTTPCodeModel}
        for code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
    },
    # Para en caso de usar projection, no devolver campos nulos
    response_model_exclude_none=True,
)
async def get_backend_by_bid(
    bid: Annotated[
        str,
        Path(
            title="The BID (Backend Identifier)",
        ),
    ],
    projection: Annotated[
        dict,
        Body(title="Projection", description="Projection of the backend", embed=True),
    ] = {},
) -> dict:
    """
    Get a single backend.

    - **bid**: The BID (Backend Identifier).
    - **returns**: The backend
    - **raises**: HTTPException 400: If the BID does not exist.
    - **raises**: HTTPException 404: If the backend is not found.
    """

    if (
        backend := db_find_backend(filter={"bid": bid}, projection=projection)
    ) is not None:
        backend = retrieve_backend(Backend(backend=backend), as_dict=True)
        return backend

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Backend with {bid} not found"
    )


@router.post(
    "/refresh",
    description="Refresh backends",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def refresh_backends_api(
    filter: Annotated[
        dict, Body(title="Filter", description="Filter the backends", embed=True)
    ] = {},
):
    """
    Get backends (filtered and/or projected).
    - **filter**: Filter to query the backends.
    - **projection**: Filter to select which fields to return.
    - **returns**: All backends.
    """
    if not filter:
        filter.update({"from_third_party": False})

    if "_id" in filter:
        filter["_id"] = sf_parse_object_id(filter["_id"])

    providers = db_find_providers(filter=filter)
    providers = list(map(lambda p: BaseProviderModel(**p), providers))

    filtered_providers: list[BaseProviderModel] = []
    # Si alguno de los proveedores es de terceros,
    # se elimina y se añade la plataforma que lo provee
    for provider in providers:
        if provider.pid.split(".")[0] in [e.value.lower() for e in ThirdPartyEnum]:
            tp_provider = BaseProviderModel(
                **db_find_provider(
                    filter={
                        "_id": sf_parse_object_id(provider.third_party.third_party_id)
                    }
                )
            )
            # Si el proveedor ya está en la lista, no se añade
            if not any(tp_provider.id == p.id for p in filtered_providers):
                filtered_providers.append(tp_provider)
        else:
            filtered_providers.append(provider)

    for provider in filtered_providers:
        logger.info(f"Processing provider: {provider.name} with id: {provider.id}...")
        refresh_backends(provider)
