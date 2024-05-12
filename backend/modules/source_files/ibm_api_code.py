from typing import Any

import requests
from modules.api_module import APIRequest, get_auth_if_needed


def get_backends(request: APIRequest) -> list[dict[str, Any]]:
    base_url = request.base_url
    auth = get_auth_if_needed(request, provider_key="ibm")
    # Obtenemos los backends
    backends = requests.get(
        f"{base_url}/backends",
        headers={"Authorization": auth},
    ).json()["devices"]

    output = []
    # Los simuladores de IBM serán retirados proximamente, por lo que no se incluirán
    backends = list(filter(lambda back: "simulator" not in back, backends))
    for backend in backends:
        # Obtenemos el estado del backend
        status = requests.get(
            f"{base_url}/backends/{backend}/status",
            headers={"Authorization": auth},
        ).json()

        # Obtenemos las propiedades del backend
        sys_props = requests.get(
            f"{base_url}/backends/{backend}/properties",
            headers={"Authorization": auth},
        ).json()

        # Obtenemos la configuración del backend
        sys_conf = requests.get(
            f"{base_url}/backends/{backend}/configuration",
            headers={"Authorization": auth},
        ).json()

        # Formateamos la configuración
        conf = {
            "basis_gates": sys_conf["basis_gates"],
            "clops_h": sys_conf["clops_h"],
            "credits_required": sys_conf["credits_required"],
            "description": sys_conf["description"],
            "max_experiments": sys_conf["max_experiments"],
            "max_shots": sys_conf["max_shots"],
        }

        # Definimos el esquema de salida
        schema = {
            "provider": None,
            "backend": backend,
            "status": status["message"],
            "qubits": sys_conf["n_qubits"],
            "queue": status["length_queue"],
            "last_updated": sys_props["last_update_date"],
            "extra": conf,
        }
        output.append(schema)

    return output
