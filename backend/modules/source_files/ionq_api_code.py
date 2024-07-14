from typing import Any

import requests
from modules.api_module import APIRequest, get_auth_if_needed


def process_backend(backend: dict) -> dict:
    backend_name = backend["backend"]
    # Si no es un simulador, obtenemos su caracterización
    if backend_name == "simulator":
        return backend
    # Eliminamos el antiguo enlace
    del backend["characterization_url"]
    # Recuperamos la caracterización
    charact: dict = requests.get(
        f"{backend['characterization_url']}",
        headers={"Authorization": backend["auth"]},
    ).json()
    # No me interesa la conectividad
    charact.pop("connectivity", None)


def get_backends(request: APIRequest) -> list[dict[str, Any]]:
    base_url = request.base_url
    try:
        auth = get_auth_if_needed(request, provider_key="ionq")
    except ValueError as err:
        print("Exception:", err)
        return []
    # Obtenemos los backends
    backends = requests.get(
        f"{base_url}/backends",
        params={"status": "verbose"},
        headers={"Authorization": auth},
    ).json()

    for idx, backend in enumerate(backends):
        backend_name = backend["backend"]
        backend["provider"] = None
        # Si no es un simulador, obtenemos su caracterización
        if backend_name == "simulator":
            continue
        # Eliminamos el antiguo enlace
        del backends[idx]["characterization_url"]
        # Recuperamos la caracterización
        charact: dict = requests.get(
            f"{base_url}/characterizations/backends/{backend_name}/current",
            headers={"Authorization": auth},
        ).json()
        # No me interesa la conectividad
        charact.pop("connectivity", None)
        # No me interesa el id
        charact.pop("id", None)
        # No me interesa otro nombre del backend
        charact.pop("backend", None)
        # TODO: Formatear la fecha a un formato generico
        charact["date"] = charact["date"]
        # Insertamos la caracterización
        backends[idx]["extra"] = {
            "characterization": charact
        }
    return backends
