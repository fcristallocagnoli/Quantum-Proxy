import os
from bson import ObjectId
from dotenv import dotenv_values
from pymongo import MongoClient, ReturnDocument
from pymongo.collection import Collection
from pymongo.cursor import Cursor

from security.aes_cipher import decrypt_data, encrypt_data

# Cuidado con variables de entorno.
# Avisar al usuario de que debe tener un archivo .env
# O proporcionar valores por defecto en caso de que no exista

config = {**dotenv_values(), **os.environ}

if not (DB_URI := config.get("DB_URI")):
    raise ValueError("DB_URI can't be empty")

DB_PORT = config.get("DB_PORT", 27017)

# Client for the database
db_client = MongoClient(DB_URI, int(DB_PORT))

# Available databases
db_test = db_client["test-database"]
db_prod = db_client["quantum-proxy-db"]

# Collections
varios_coll = db_test.varios

providers_coll = db_prod.providers
backends_coll = db_prod.backends
characts_coll = db_prod.characts
users_coll = db_prod.users

# region Misc ----------------------------


# check if a collection is empty
def is_empty(collection: str) -> bool:
    coll = {
        "providers": providers_coll,
        "backends": backends_coll,
        "users": users_coll,
    }.get(collection, None)
    if coll is None:
        raise ValueError(f"Collection '{collection}' not found")
    return coll.count_documents({}) == 0


# count the number of documents in a collection
def count_documents(collection: str) -> int:
    """
    Count the number of documents in a collection.
    :param collection: <str> collection to count
    :return: <int> number of documents in the collection
    """
    coll = {
        "providers": providers_coll,
        "backends": backends_coll,
        "users": users_coll,
    }.get(collection, None)
    if coll is None:
        raise ValueError(f"Collection '{collection}' not found")
    return coll.count_documents({})


# region Generic ----------------------------


def aggregate(*, collection: str, pipeline: list[dict]) -> Cursor:
    """
    Perform an aggregation on the collection.
    :param ``collection``: collection on which to aggregate
    :param ``pipeline``: list of aggregation stages
    """
    coll = {
        "providers": providers_coll,
        "backends": backends_coll,
        "users": users_coll,
    }.get(collection, None)
    if coll is None:
        raise ValueError(f"Collection '{collection}' not found")
    return coll.aggregate(pipeline)


def db_find_one(
    collection: Collection, *, filter: ObjectId | dict = None, projection: dict = {}
) -> dict:
    """
    Get the provider matching the id or query a document.
    :param ``collection``: collection from which to query
    :param ``filter`` (optional): a dictionary specifying the query to be performed
    OR any other type to be used as the value for a query for ``"_id"``
    :param ``projection`` (optional): fields to include or exclude in the result
    """
    if isinstance(filter, ObjectId):
        return collection.find_one(filter, projection)
    elif isinstance(filter, dict):
        return collection.find_one(filter, projection)
    else:
        return None


def db_find_many(
    collection: Collection, *, filter: dict = {}, projection: dict = {}
) -> Cursor:
    """
    Get the provider matching the id or query a document.
    :param ``collection``: collection from which to query
    :param ``filter`` (optional): a dictionary specifying the query to be performed
    OR any other type to be used as the value for a query for ``"_id"``
    :param ``projection`` (optional): fields to include or exclude in the result
    """
    return collection.find(filter, projection)


def db_insert_one(collection: Collection, document: dict) -> str:
    """
    Insert a new document into the database.
    :param ``collection``: collection in which to insert
    :param ``document``: dict
    :return: Inserted ID (str)
    """
    return collection.insert_one(document).inserted_id


def db_insert_many(collection: Collection, documents: list[dict]) -> list[str]:
    """
    Insert a list of documents into the database.
    :param ``collection``: collection in which to insert
    :param ``documents``: list of dicts
    :return: List of inserted IDs (list[str])
    """
    return collection.insert_many(documents).inserted_ids


def db_update_one(collection: Collection, *, filter: dict, cambios: dict):
    """
    Updates a single document matching the filter.
    :param ``collection``: collection in which to update
    :param filter: query document
    :param cambios: dict with the changes to apply
    """
    return collection.find_one_and_update(
        filter, cambios, return_document=ReturnDocument.AFTER
    )


def db_update_many(collection: Collection, *, filter: dict, cambios: dict):
    """
    Updates a single document matching the filter.
    :param ``collection``: collection in which to update
    :param filter: query document
    :param cambios: dict with the changes to apply
    """
    return collection.update_many(filter, cambios)


def db_replace_one(
    collection: Collection, *, filter: dict, replacement: dict, **kwargs
) -> dict:
    """
    Replaces a single document matching the filter.
    :param ``collection``: collection in which to replace
    :param filter: query document
    :param replacement: document to replace
    """
    return collection.find_one_and_replace(
        filter, replacement, kwargs, return_document=ReturnDocument.AFTER
    )


def db_delete_one(collection: Collection, *, filter: dict) -> bool:
    """
    Deletes a single document matching the filter.
    :param ``collection``: collection in which to delete
    :param filter: query document
    :return: True if the document was deleted, False otherwise
    """
    # return collection.find_one_and_delete(filter)
    return collection.delete_one(filter).deleted_count == 1


def db_delete_many(collection: Collection, *, filter: dict) -> bool:
    """
    Deletes all documents matching the filter.
    :param ``collection``: collection in which to delete
    :param filter: query document
    :return: True if at least one document was deleted, False otherwise
    """
    return collection.delete_many(filter).deleted_count > 0


# region Users ----------------------------


def db_find_user(*, filter: ObjectId | dict = None, projection: dict = {}) -> dict:
    """
    Get the user matching the id or query a document.
    :param ``filter`` (optional): a dictionary specifying the query to be performed
    OR any other type to be used as the value for a query for ``"_id"``
    :param ``projection`` (optional): fields to include or exclude in the result
    """
    user = db_find_one(users_coll, filter=filter, projection=projection)
    if user and (api_keys := user.get("api_keys", None)):
        user["api_keys"] = decrypt_api_keys(api_keys)
    return user


def db_find_users(*, filter: dict = {}, projection: dict = {}) -> Cursor:
    """
    Get all users that match the filter.
    :param filter: query document
    """
    users = list(db_find_many(users_coll, filter=filter, projection=projection))
    for user in users:
        if api_keys := user.get("api_keys", None):
            user["api_keys"] = decrypt_api_keys(api_keys)
    return users


def db_insert_user(user: dict) -> str:
    """
    Insert a new user into the database.
    :param user: dict
    :return: Inserted ID (str)
    """
    if api_keys := user.get("api_keys", None):
        user["api_keys"] = encrypt_api_keys(api_keys)
    return db_insert_one(users_coll, user)


def db_update_user(*, filter: dict, cambios: dict):
    """
    Updates a single user matching the filter.
    :param filter: user query
    :param cambios: dict with the changes to apply
    """
    if cambios.get("$set", None) and (
        api_keys := cambios["$set"].get("api_keys", None)
    ):
        cambios["$set"]["api_keys"] = encrypt_api_keys(api_keys)
    return db_update_one(users_coll, filter=filter, cambios=cambios)


def db_delete_user(*, filter: dict) -> bool:
    """
    Deletes a single user matching the filter.
    :param filter: user query
    """
    return db_delete_one(users_coll, filter=filter)


# region Providers ----------------------------


def db_find_provider(*, filter: ObjectId | dict = None, projection: dict = {}) -> dict:
    """
    Get the provider matching the id or query a document.
    :param ``filter`` (optional): a dictionary specifying the query to be performed
    OR any other type to be used as the value for a query for ``"_id"``
    :param ``projection`` (optional): fields to include or exclude in the result
    """
    return db_find_one(providers_coll, filter=filter, projection=projection)


def db_find_providers(*, filter: dict = {}, projection: dict = {}) -> Cursor:
    """
    Get all providers that match the filter.
    :param filter: query document
    """
    return db_find_many(providers_coll, filter=filter, projection=projection)


def db_aggregate_providers(*, pipeline: list[dict]) -> Cursor:
    """
    Perform an aggregation on the providers collection.
    :param pipeline: list of aggregation stages
    """
    return aggregate(providers_coll, pipeline=pipeline)


def db_insert_provider(provider) -> str:
    """
    Insert a new provider into the database.
    :param provider: dict
    :return: Inserted ID (str)
    """
    return db_insert_one(providers_coll, provider)


def db_insert_providers(providers: list[dict]) -> str:
    """
    Insert a list of providers into the database.
    :param providers: list of dicts
    :return: List of inserted IDs (list[str])
    """
    return db_insert_many(providers_coll, providers)


def db_update_provider(*, filter: dict, cambios: dict):
    """
    Updates a single provider matching the filter.
    :param filter: provider query
    :param cambios: dict with the changes to apply
    """
    return db_update_one(providers_coll, filter=filter, cambios=cambios)


def db_update_providers(*, filter: dict, cambios: dict):
    """
    Updates all providers matching the filter.
    :param filter: provider query
    :param cambios: dict with the changes to apply
    """
    return db_update_many(providers_coll, filter=filter, cambios=cambios)


def db_replace_provider(*, filter: dict, replacement: dict) -> dict:
    """
    Replaces a single provider matching the filter.
    :param filter: provider query
    :param replacement: provider to replace
    """
    return db_replace_one(providers_coll, filter=filter, replacement=replacement)


def db_delete_provider(*, filter: dict) -> bool:
    """
    Deletes a single provider matching the filter.
    :param filter: provider query
    """
    return db_delete_one(providers_coll, filter=filter)


def db_delete_providers(*, filter: dict) -> bool:
    """
    Deletes all providers matching the filter.
    :param filter: provider query
    """
    return db_delete_many(providers_coll, filter=filter)


# region Backends ----------------------------


def db_find_backend(*, filter: ObjectId | dict = None, projection: dict = {}) -> dict:
    """
    Get the backend matching the id or query a document.
    :param ``filter`` (optional): a dictionary specifying the query to be performed
    OR any other type to be used as the value for a query for ``"_id"``
    :param ``projection`` (optional): fields to include or exclude in the result
    """
    if projection:
        projection.update({"class_type": 1})
    return db_find_one(backends_coll, filter=filter, projection=projection)


def db_find_backends(*, filter: dict = {}, projection: dict = {}) -> Cursor:
    """
    Get all backends that match the filter.
    :param filter: query document
    """
    if projection:
        projection.update({"class_type": 1})
    return db_find_many(backends_coll, filter=filter, projection=projection)


def db_insert_backend(backend: dict) -> str:
    """
    Insert a new backend into the database.
    :param backend: dict
    :return: Inserted ID (str)
    """
    return db_insert_one(backends_coll, backend)


def db_insert_backends(backends: list[dict]) -> list[str]:
    """
    Insert a list of backends into the database.
    :param backends: list of dicts
    :return: List of inserted IDs (list[str])
    """
    return db_insert_many(backends_coll, backends)


def db_update_backend(*, filter: dict, cambios: dict):
    """
    Updates a single backend matching the filter.
    :param filter: backend query
    :param cambios: dict with the changes to apply
    """
    return db_update_one(backends_coll, filter=filter, cambios=cambios)


def db_update_backends(*, filter: dict, cambios: dict):
    """
    Updates all backends matching the filter.
    :param filter: backend query
    :param cambios: dict with the changes to apply
    """
    return db_update_many(backends_coll, filter=filter, cambios=cambios)


def db_delete_backend(*, filter: dict) -> bool:
    """
    Deletes a single backend matching the filter.
    :param filter: backend query
    """
    return db_delete_one(backends_coll, filter=filter)


def db_delete_backends(*, filter: dict) -> bool:
    """
    Deletes all backends matching the filter.
    :param filter: backend query
    """
    return db_delete_many(backends_coll, filter=filter)


# region Helpers ----------------------------


def decrypt_api_keys(api_keys: dict[str, dict]):
    for platform, secrets in api_keys.items():
        api_keys[platform] = {
            key: decrypt_data(value) for key, value in secrets.items()
        }
    return api_keys


def encrypt_api_keys(api_keys: dict[str, dict]):
    for platform, secrets in api_keys.items():
        api_keys[platform] = {
            key: encrypt_data(value) for key, value in secrets.items()
        }
    return api_keys
