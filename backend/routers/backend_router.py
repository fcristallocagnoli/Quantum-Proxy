from typing import Annotated

from database.models.backends_models import Backend, retrieve_backend
from database.mongo_client import db_find_backend, db_find_backends
from fastapi import APIRouter, Body, HTTPException, Path, status
from pydantic import BaseModel

from routers.provider_router import sf_parse_object_id


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
    backends = list(
        map(
            lambda b: retrieve_backend(Backend(backend=b), as_dict=True),
            db_find_backends(filter=filter, projection=projection),
        )
    )
    return backends


@router.get(
    "/{id}",
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
async def get_backend_by_id(
    id: Annotated[
        str,
        Path(
            title="The ID of the backend",
        ),
    ],
    projection: Annotated[
        dict,
        Body(title="Projection", description="Projection of the backend", embed=True),
    ] = {},
) -> dict:
    """
    Get a single backend.

    - **id**: The ID of the backend.
    - **returns**: The backend
    - **raises**: HTTPException 400: If the id does not exist.
    - **raises**: HTTPException 404: If the backend is not found.
    """

    if (
        backend := db_find_backend(filter=sf_parse_object_id(id), projection=projection)
    ) is not None:
        backend = retrieve_backend(Backend(backend=backend), as_dict=True)
        return backend

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Backend with {id} not found"
    )
