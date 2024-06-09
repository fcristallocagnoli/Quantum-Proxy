from bson import ObjectId
from fastapi.logger import logger
from database.models.providers_models import BaseProviderModel, ThirdPartyEnum
from modules.gateway_module import fetch_data
from database.provider_data import providers_data
from database.mongo_client import (
    db_delete_backends,
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


def init_providers():
    db_insert_providers(providers_data)

    for third_party in [e.value for e in ThirdPartyEnum]:
        formated_tp = third_party.lower().replace(" ", "_")
        provider = db_find_provider(filter={"pid": f"native.{formated_tp}"})
        db_update_providers(
            filter={"third_party.third_party_name": third_party},
            cambios={"$set": {"third_party.third_party_id": provider["_id"]}},
        )


def refresh_backends(provider: BaseProviderModel):
    """
    Refreshes the backends of a provider

    Args:
    - provider (BaseProviderModel): The provider to refresh
        - id (str): The provider's database id
    """
    old_ids = list(map(lambda id: ObjectId(id), provider.backends_ids))
    db_delete_backends(filter={"_id": {"$in": old_ids}})

    datos = fetch_data(provider)
    backends_ids = db_insert_backends(datos)

    db_update_provider(
        filter={"_id": ObjectId(provider.id)},
        cambios={"$set": {"backends_ids": backends_ids}},
    )


def init_backends(scheduler: BackgroundScheduler):
    providers = db_find_providers(filter={"from_third_party": False})
    providers = list(map(lambda p: BaseProviderModel(**p), providers))
    for provider in providers:
        logger.info(f"Processing provider: {provider.name} with id: {provider.id}...")
        scheduler.add_job(func=refresh_backends, args=[provider], id=provider.name)
