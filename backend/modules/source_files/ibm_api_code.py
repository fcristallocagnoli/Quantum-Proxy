from typing import Any

import requests
from database.mongo_client import db_find_provider
from modules.api_module import APIRequest, get_auth_if_needed
from utils.utils import norm_id


def get_backends(request: APIRequest) -> list[dict[str, Any]]:
    base_url = request.base_url
    auth = get_auth_if_needed(request, provider_code="ibm")
    # Obtenemos los backends
    backends = requests.get(
        f"{base_url}/backends",
        headers={"Authorization": auth},
    ).json()["devices"]

    output = []
    # Los simuladores de IBM serán retirados proximamente, por lo que no se incluirán
    backends = list(filter(lambda back: "simulator" not in back, backends))
    # i = 0
    # total = time.time()
    for backend in backends:
        # iteracion = time.time()
        # inicio = time.time()
        # backend["extra"] = {
        #     "characterization": insert_characterization(
        #         f"{self.name.lower()}_{backend['backend_name'].lower()}", backend
        #     ).inserted_id
        # }
        # TODO: Ver si se puede paralelizar
        status = requests.get(
            f"{base_url}/backends/{backend}/status",
            headers={"Authorization": auth},
        ).json()
        # print(f"Tenemos status, backend n{i} en", time.time()-inicio)
        # inicio = time.time()

        sys_props = requests.get(
            f"{base_url}/backends/{backend}/properties",
            headers={"Authorization": auth},
        ).json()
        # print(f"Tenemos sys_props, backend n{i} en", time.time()-inicio)
        # inicio = time.time()

        sys_conf = requests.get(
            f"{base_url}/backends/{backend}/configuration",
            headers={"Authorization": auth},
        ).json()
        # print(f"Tenemos sys_conf, backend n{i} en", time.time()-inicio)

        conf = {
            "basis_gates": sys_conf["basis_gates"],
            "clops_h": sys_conf["clops_h"],
            "credits_required": sys_conf["credits_required"],
            "description": sys_conf["description"],
            "max_experiments": sys_conf["max_experiments"],
            "max_shots": sys_conf["max_shots"],
        }
        # print(status)
        schema = {
            "provider": {
                "provider_id": norm_id(db_find_provider(filter={"name": "IBM Quantum"})),
                "provider_name": "IBM Quantum",
            },
            "backend": backend,
            "status": status["message"],
            "qubits": sys_conf["n_qubits"],
            "queue": status["length_queue"],
            "last_updated": sys_props["last_update_date"],
            "extra": conf,
        }
        output.append(schema)
    #     print(f"Iteración {i} finalizada en", time.time()-iteracion, "\n")
    #     i+=1
    # print("Total finalizado en", time.time()-total)

    return output