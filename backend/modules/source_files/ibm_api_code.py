from typing import Any

import requests

from utils.email_utils import send_error_mail
from modules.api_module import APIRequest, get_auth_if_needed


def get_backends(request: APIRequest) -> list[dict[str, Any]]:
    base_url = request.base_url
    try:
        auth = get_auth_if_needed(request, provider_key="ibm")
    except ValueError as err:
        print("Exception:", err)
        return []
    # Obtenemos los backends
    try:
        backend_response = requests.get(
            f"{base_url}/backends",
            headers={"Authorization": auth},
        ).json()
        backends = backend_response["devices"]
    # IBM está teniendo problemas con sus API Keys,
    # a veces hay que regenerarlas porque las antiguas no funcionan
    except Exception as err:
        print("Error fetching IBM backends:", err, "\nwith response:", backend_response)
        send_error_mail(backend_response, context="Error fetching IBM backends")
        return []

    # Los simuladores de IBM serán retirados proximamente, por lo que no se incluirán
    backends = list(filter(lambda back: "simulator" not in back, backends))

    output = []
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


def main():
    backend_request = {
        "fetch_method": "API",
        "base_url": "https://api.quantum-computing.ibm.com/runtime",
        "auth": {"Authorization": "Bearer TOKEN"},
        "module": {"func_to_eval": "get_backends", "module_file": "ibm_api_code"},
    }
    result = get_backends(backend_request)
    print(result)


if __name__ == "__main__":
    main()
