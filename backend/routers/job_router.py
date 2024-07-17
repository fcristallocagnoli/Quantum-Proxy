from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Response, status
from modules.job_module import create_job, delete_job, get_job, get_job_output, get_jobs
from pydantic import BaseModel


# For documentation purposes
class HTTPCodeModel(BaseModel):
    detail: str = None


router = APIRouter(tags=["Jobs"], prefix="/jobs")


@router.post(
    "/get",
    description="List jobs (filtered and/or projected)",
    response_model=list[dict],
    response_model_by_alias=False,
    # Para en caso de usar projection, no devolver campos nulo
    response_model_exclude_none=True,
)
async def get_all_jobs(
    api_keys: Annotated[dict, Body(..., embed=True)] = {},
) -> list[dict]:
    """
    Get jobs.
    - **api_keys**: The secret keys.
    - **returns**: All jobs.
    """
    jobs: list = []
    for platform, keys in api_keys.items():
        # Lista de proveedores que soportan envio de trabajos
        if platform in ["ionq"]:
            jobs.extend(get_jobs(platform, keys))
    return jobs


@router.post(
    "/get/{uuid}",
    description="Get a single job",
    response_model=dict,
    response_model_by_alias=False,
    responses={
        code: {"model": HTTPCodeModel}
        for code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
    },
    # Para en caso de usar projection, no devolver campos nulos
    response_model_exclude_none=True,
)
async def get_single_job(
    uuid: Annotated[
        str,
        Path(
            title="The job UUID",
        ),
    ],
    api_keys: dict = Body(..., embed=True),
) -> dict:
    """
    Get a single job.

    - **uuid**: The job UUID.
    - **api_keys**: The secret keys.
    - **returns**: The job.
    - **raises**: HTTPException 400: If the UUID does not exist.
    - **raises**: HTTPException 404: If the job is not found.
    """

    for platform, keys in api_keys.items():
        # Lista de proveedores que soportan envio de trabajos
        if platform in ["ionq"]:
            if job := get_job(uuid, platform, keys):
                return job

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with {uuid} not found"
    )


@router.post(
    "/results/{uuid}",
    description="Get a job-s output",
    response_model=dict,
    response_model_by_alias=False,
    responses={
        code: {"model": HTTPCodeModel}
        for code in [status.HTTP_400_BAD_REQUEST, status.HTTP_404_NOT_FOUND]
    },
    # Para en caso de usar projection, no devolver campos nulos
    response_model_exclude_none=True,
)
async def get_single_job_ouput(
    uuid: Annotated[
        str,
        Path(
            title="The job UUID",
        ),
    ],
    api_keys: dict = Body(..., embed=True),
) -> dict:
    """
    Get a job's output.

    - **uuid**: The job UUID.
    - **api_keys**: The secret keys.
    - **returns**: The job's output.
    - **raises**: HTTPException 400: If the UUID does not exist.
    - **raises**: HTTPException 404: If the job is not found.
    """

    for platform, keys in api_keys.items():
        # Lista de proveedores que soportan envio de trabajos
        if platform in ["ionq"]:
            if job := get_job_output(uuid, platform, keys):
                return job

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with {uuid} not found"
    )


@router.post(
    "/create",
    description="Add new job",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    responses={
        status.HTTP_201_CREATED: {"model": dict},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_409_CONFLICT: {"model": HTTPCodeModel},
    },
)
async def post_job(
    job: dict = Body(...),
    api_keys: dict = Body(...),
) -> dict:
    """
    Create a new job.

    - **job**: The job to create.
    - **returns**: HTTP 201 Created: The job created.
    - **raises**: HTTPException 409: If the job already exists.
    """

    status_code = create_job(job, api_keys)

    if status_code == 200:
        return Response(status_code=status.HTTP_201_CREATED)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Job failed to create with status code {status_code}",
    )


@router.post(
    "/delete/{uuid}",
    description="Delete a job",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "No Content"},
        status.HTTP_400_BAD_REQUEST: {"model": HTTPCodeModel},
        status.HTTP_404_NOT_FOUND: {"model": HTTPCodeModel},
    },
)
async def delete_single_job(
    uuid: Annotated[
        str,
        Path(
            title="The job UUID",
        ),
    ],
    api_keys: dict = Body(..., embed=True),
):
    """
    Delete a single job.

    - **uuid**: The job UUID
    - **api_keys**: The secret keys.
    - **returns**: HTTP 204 No Content
    - **raises**: HTTPException 404: If the job is not found.
    """
    for platform, keys in api_keys.items():
        # Lista de proveedores que soportan envio de trabajos
        if platform in ["ionq"]:
            if delete_job(uuid, platform, keys) == status.HTTP_200_OK:
                return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with {uuid} not found"
    )


# # region Utils ----------------------------


# def sf_parse_object_id(id: str) -> ObjectId:
#     """
#     Safe parse from str to ObjectId.
#     :raises HTTPException 400: if the id is not valid
#     """
#     try:
#         object_id = ObjectId(id)
#         return object_id
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id {e}"
#         )
