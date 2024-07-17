import requests


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
            return None



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
    keys = api_keys["ionq"]
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
        }
    }
    job_status = requests.post(
        f"{base_url}/jobs",
        json=ionq_job,
        headers={"Authorization": f"apiKey {keys["TOKEN"]}"},
    ).status_code
    return job_status


def delete_job_from_ionq(uuid: str, keys: dict):
    base_url = "https://api.ionq.co/v0.3"
    job = requests.delete(
        f"{base_url}/jobs/{uuid}",
        headers={"Authorization": f"apiKey {keys["TOKEN"]}"},
    )
    return job.status_code
