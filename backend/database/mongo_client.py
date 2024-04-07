from bson import ObjectId
from dotenv import dotenv_values
from pymongo import MongoClient
from pymongo.cursor import Cursor

config = dotenv_values()

# Client for the database
db_client = MongoClient(config["DB_HOST"], int(config["DB_PORT"]))

# Available databases
db_test = db_client["test-database"]
db_prod = db_client["quantum-proxy-db"]

# Collections
users_coll = db_test.users
varios_coll = db_test.varios

providers_coll = db_prod.providers
backends_coll = db_prod.backends
characts_coll = db_prod.characts

# Providers ----------------------------


def db_find_provider(
    *, obj_id: ObjectId = None, filter: dict = None, projection: dict = {}
) -> dict:
    """
    Get the provider matching the id or query a document.
    :param obj_id: ObjectId of the document
    :param filter: query document
    """
    # Se da prioridad al obj_id
    if obj_id:
        return providers_coll.find_one(obj_id, projection)
    # Si no se proporciona obj_id, se busca por el filtro
    elif filter:
        return providers_coll.find_one(filter, projection)
    else:
        return None


def db_find_providers(*, filter={}, projection={}) -> Cursor:
    """
    Get all providers that match the filter.
    :param filter: query document
    """
    return providers_coll.find(filter, projection)


def db_insert_provider(provider) -> str:
    """
    Insert a new provider into the database.
    :param provider: dict
    :return: Inserted ID (str)
    """
    return str(providers_coll.insert_one(provider).inserted_id)


def db_find_and_update_provider(*, filter, cambios: dict):
    """
    Updates a single document matching the filter.
    :param filter: query document
    :param cambios: dict with the changes to apply
    """
    return providers_coll.find_one_and_update(filter, update=cambios)


def db_find_and_replace_provider(*, filter, replacement: dict) -> dict:
    """
    Replaces a single document matching the filter.
    :param filter: query document
    :param replacement: provider to replace
    """
    return providers_coll.find_one_and_replace(filter, replacement=replacement)


def db_find_and_delete_provider(*, filter: dict) -> dict:
    """
    Deletes a single document matching the filter.
    :param filter: query document
    """
    return providers_coll.find_one_and_delete(filter)


# ---------------------------- Providers
