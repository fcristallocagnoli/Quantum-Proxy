import importlib.util
from pathlib import Path

from bson import ObjectId
from database.models.providers_models import APIRequest, BaseProviderModel
from database.models.user_models import UserModel
from database.mongo_client import db_find_user
from dotenv import dotenv_values
from utils.utils import check_code

env = dotenv_values()

DUMMY_ACCOUNT = env["DUMMY_ACCOUNT"]


def get_auth_if_needed(request: APIRequest, *, provider_key: str):
    if auth_format := request.auth.get("Authorization", None):
        user = db_find_user(filter={"email": DUMMY_ACCOUNT})
        assert user, "User not found"
        user = UserModel(**user)
        db_api_keys = user.api_keys.get(provider_key)
        auth = auth_format.replace("TOKEN", db_api_keys.get("TOKEN"))
        return auth


def fetch_from_api(provider: BaseProviderModel) -> list[dict]:
    """
    Fetches the backends from the provider's API

    Returns:
    - list[dict]: A list of backends
    """
    print("Fetching from API...")
    module = provider.backend_request.module
    func = module.func_to_eval
    file_name = module.module_file
    file_path = (
        Path(__file__).parent.joinpath("source_files").joinpath(f"{file_name}.py")
    )

    if not check_code(file_path):
        return []

    # Importamos el módulo dinámicamente desde el archivo externo
    especificacion = importlib.util.spec_from_file_location(file_name, file_path)
    modulo = importlib.util.module_from_spec(especificacion)
    especificacion.loader.exec_module(modulo)

    # Ejecutamos la función designada y obtenemos los datos
    raw_output: list[dict] = getattr(modulo, func)(provider.backend_request)

    provider_data = {
        "provider_id": ObjectId(provider.id),
        "provider_name": provider.name,
    }
    raw_output = list(
        map(
            lambda back: back.update({"provider": provider_data}) or back,
            raw_output,
        )
    )

    return raw_output
