from typing import Any

import requests
from database.mongo_client import db_find_provider
from modules.api_module import APIRequest, get_auth_if_needed
from utils.utils import norm_id


def get_backends(request: APIRequest) -> list[dict[str, Any]]:

    base_url = request.base_url
    auth = get_auth_if_needed(request, provider_code="ionq")
    # Obtenemos los backends
    backends = requests.get(
        f"{base_url}/backends",
        params={"status": "verbose"},
        headers={"Authorization": auth},
    ).json()

    # Iteramos sobre los backends para obtener la ultima caracterización
    # de cada uno y guardarla en la base de datos
    for idx, backend in enumerate(backends):
        backend_name = backend["backend"]
        # Si no es un simulador, obtenemos su caracterización
        backend["provider"] = {
            "provider_id": norm_id(db_find_provider(filter={"name": "IonQ"})),
            "provider_name": "IonQ",
        }
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
        # TODO: Formatear la fecha a un formato generico
        charact["date"] = charact["date"]
        # Insertamos la caracterización en la base de datos
        # y guardamos el ObjectId en el campo extra como referencia
        backends[idx]["extra"] = {
            # "characterization": insert_characterization(
            #     f"{self.name.lower()}_{backend_name.lower()}", charact
            # ).inserted_id
            # "characterization_id": f"{"IonQ".lower()}_{backend_name.lower()}",
            "characterization_id": f"ionq.{charact["backend"]}",
            "characterization": charact
        }
    # Guardamos los backends en la base de datos
    # provider: dict = {
    #     "id": str(find_provider_by_name(ProviderName.IONQ)["_id"]),
    #     "name": ProviderName.IONQ,
    # }
    # for backend in backends:
    #     insert_backend({"provider": provider, **backend})
    return backends