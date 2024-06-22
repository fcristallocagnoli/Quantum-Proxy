from bson import ObjectId
from fastapi.logger import logger
from utils.utils import get_current_datetime, get_wiki_content
from database.models.providers_models import BaseProviderModel, ThirdPartyEnum
from modules.gateway_module import fetch_data
from database.provider_data import providers_data
from database.scripts.extra_data import get_extra_data
from database.mongo_client import (
    db_delete_backends,
    db_find_backends,
    db_find_provider,
    db_find_providers,
    db_insert_backends,
    db_insert_providers,
    db_update_provider,
    db_update_providers,
)
from apscheduler.schedulers.background import BackgroundScheduler


def job_manager(event):
    if event.exception:
        logger.error(f"Job {event.job_id} failed with exception {event.exception}")
        return
    logger.debug(f"Job {event.job_id} executed successfully")


def pre_process_providers(provider_list: list[dict]):
    # rellenar con contenido de wikipedia (si procede)
    for provider in provider_list:
        if provider["wiki_name"]:
            provider.update({"description": get_wiki_content(provider["wiki_name"])})
    return provider_list


def post_process_providers():
    # Actualizar los ids de los proveedores de terceros
    for third_party in [e.value for e in ThirdPartyEnum]:
        formated_tp = third_party.lower().replace(" ", "_")
        provider = db_find_provider(filter={"pid": f"native.{formated_tp}"})
        db_update_providers(
            filter={"third_party.third_party_name": third_party},
            cambios={"$set": {"third_party.third_party_id": provider["_id"]}},
        )
    # Añadir datos extra que no se pueden automatizar:
    # - descripciones
    extra_data: dict = get_extra_data()
    for name, data in extra_data.items():
        db_update_providers(filter={"name": name}, cambios={"$set": data})


def init_providers():
    # Insertamos los proveedores
    db_insert_providers(providers_data)
    # Procesamos los proveedores una vez insertados
    post_process_providers()


def refresh_backends(provider: BaseProviderModel):
    """
    Refreshes the backends of a provider

    Args:
    - provider (BaseProviderModel): The provider to refresh
        - id (str): The provider's database id
    """
    # Borramos los backends antiguos
    old_ids = list(map(lambda id: ObjectId(id), provider.backends_ids))
    db_delete_backends(filter={"_id": {"$in": old_ids}})

    # Borramos las referencias a los backends antiguos
    db_update_providers(
        filter={"backends_ids": {"$in": old_ids}},
        cambios={"$set": {"backends_ids": []}},
    )

    # Obtenemos los nuevos backends
    datos = fetch_data(provider)
    backends_ids = db_insert_backends(datos)

    # Si el proveedor es de terceros, hay que actualizar los proveedores que ofrece
    if provider.pid.split(".")[1] in [e.value.lower() for e in ThirdPartyEnum]:

        # Obtenemos los backends asociados
        for backend in db_find_backends(filter={"_id": {"$in": backends_ids}}):
            # Si el nombre coincide, y proviene de terceros, se añade el id del backend
            db_update_provider(
                filter={
                    "name": backend["provider"]["provider_name"],
                    "from_third_party": True,
                },
                cambios={
                    "$push": {"backends_ids": backend["_id"]},
                    "$set": {"last_checked": get_current_datetime()},
                },
            )

    # Para el resto de proveedores, se actualiza la lista de ids de backends
    db_update_provider(
        filter={"_id": ObjectId(provider.id)},
        cambios={
            "$set": {
                "backends_ids": backends_ids,
                "last_checked": get_current_datetime(),
            }
        },
    )


def init_backends(scheduler: BackgroundScheduler):
    providers = db_find_providers(filter={"from_third_party": False})
    providers = list(map(lambda p: BaseProviderModel(**p), providers))
    for provider in providers:
        logger.info(f"Processing provider: {provider.name} with id: {provider.id}...")
        scheduler.add_job(func=refresh_backends, args=[provider], id=provider.name)
