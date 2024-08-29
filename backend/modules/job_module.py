from fastapi import HTTPException, Response
from fastapi import status
import requests

from utils.email_utils import send_error_mail


def get_jobs(platform: str, keys: dict):
    match platform:
        case "ionq":
            jobs = get_jobs_from_ionq(keys)
        case _:
            return None
    return jobs


def get_job(uuid: str, platform: str, keys: dict):
    match platform:
        case "ionq":
            job = get_job_from_ionq(uuid, keys)
        case _:
            return None
    return job


def get_job_output(uuid: str, platform: str, keys: dict):
    match platform:
        case "ionq":
            job_output = get_job_output_from_ionq(uuid, keys)
        case _:
            return None
    return job_output


def create_job(job: dict, api_keys: dict):
    match job["provider"]:
        case "native.ionq":
            return create_job_on_ionq(job, api_keys)
        case _:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provider not supported"
            )



def delete_job(uuid: str, platform: str, keys: dict):
    match platform:
        case "ionq":
            return delete_job_from_ionq(uuid, keys)
        case _:
            return None


# ------------------------------

def get_jobs_from_ionq(keys: dict):
    base_url = "https://api.ionq.co/v0.3"
    jobs = requests.get(
        f"{base_url}/jobs",
        headers={"Authorization": f"apiKey {keys["TOKEN"]}"},
    ).json()
    return jobs["jobs"]


def get_job_from_ionq(uuid: str, keys: dict):
    base_url = "https://api.ionq.co/v0.3"
    job = requests.get(
        f"{base_url}/jobs/{uuid}",
        headers={"Authorization": f"apiKey {keys["TOKEN"]}"},
    ).json()
    return job


def get_job_output_from_ionq(uuid: str, keys: dict):
    base_url = "https://api.ionq.co/v0.3"
    job_output = requests.get(
        f"{base_url}/jobs/{uuid}/results",
        headers={"Authorization": f"apiKey {keys["TOKEN"]}"},
    ).json()
    return job_output


def create_job_on_ionq(job: dict, api_keys: dict):
    try:
        keys = api_keys["ionq"]
    except KeyError:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User does not have IonQ API keys",
        )
    base_url = "https://api.ionq.co/v0.3"
    ionq_job = {
        "name": job.get("name"),
        "shots": job.get("shots"),
        "target": job.get("target"),
        "input": {
            "format": "ionq.circuit.v0",
            "gateset": "qis",
            "qubits": job.get("qubits"),
            "circuit": job.get("circuit"),
        },
        "noise": {
            "model": job.get("noiseModel", "ideal"),
        }
    }
    job_response = requests.post(
        f"{base_url}/jobs",
        json=ionq_job,
        headers={"Authorization": f"apiKey {keys["TOKEN"]}"},
    )
    if job_response.status_code // 100 == 4:
        send_error_mail(
            Exception(
                f"Error {job_response.status_code} creating job on IonQ: {job_response.json()}"
            ),
            "On create_job_on_ionq function",
        )
    # return job_response.status_code
    return Response(status_code=job_response.status_code, content=job_response.text)


def delete_job_from_ionq(uuid: str, keys: dict):
    base_url = "https://api.ionq.co/v0.3"
    job = requests.delete(
        f"{base_url}/jobs/{uuid}",
        headers={"Authorization": f"apiKey {keys["TOKEN"]}"},
    )
    return job.status_code
