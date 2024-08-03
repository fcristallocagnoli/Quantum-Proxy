from typing import Annotated

from database.mongo_client import aggregate, count_documents
from fastapi import APIRouter, Body, Path, status
from pydantic import BaseModel

router = APIRouter(tags=["Helpers"], prefix="/helpers")


class HTTPCodeModel(BaseModel):
    detail: str = None


@router.post(
    "/aggregate",
    description="Aggregation result (list)",
    response_model=list[dict],
    response_model_by_alias=False,
    # Para en caso de usar projection, no devolver campos nulo
    response_model_exclude_none=True,
)
async def get_agreggation(
    collection: Annotated[
        str,
        Body(title="Collection", description="Collection to aggregate from"),
    ],
    pipeline: Annotated[
        list,
        Body(title="Pipeline", description="Pipeline to aggregate"),
    ],
) -> list[dict]:
    """
    Get aggregation.
    - **collection**: Collection to aggregate from.
    - **pipeline**: Pipeline to aggregate.
    - **returns**: All providers.
    """
    return aggregate(collection=collection, pipeline=pipeline)


@router.get(
    "/count-documents/{collection}",
    description="Count the number of documents in a collection",
    response_model=dict,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
    },
)
def count_collection(
    collection: Annotated[
        str,
        Path(
            title="The collection to count",
            description="The name of the collection to count.",
        ),
    ],
) -> dict:
    """
    Count the number of documents in a collection.
    """
    return {
        "message": f"Document count from {collection}",
        "count": count_documents(collection),
    }
