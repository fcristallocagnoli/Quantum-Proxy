# general imports
import importlib.util
import os
from pathlib import Path
from typing import Any

from database.models.providers_models import BaseProviderModel, SDKRequest
from database.models.user_models import UserModel
from database.mongo_client import db_find_user
from dotenv import dotenv_values
from utils.utils import check_code

env = {
    **dotenv_values(),
    **os.environ
}

try:
    DUMMY_ACCOUNT = env["DUMMY_ACCOUNT"]
except KeyError:
    raise ValueError("DUMMY_ACCOUNT not found in env vars")


def get_env_vars_if_needed(request: SDKRequest, *, provider_key: str):
    if env_vars := request.auth.get("env_vars", None):
        if not (user := db_find_user(filter={"email": DUMMY_ACCOUNT})):
            raise ValueError("Dummy account not found in database")
        user = UserModel(**user)
        if not (third_party_env_vars := user.api_keys.get(provider_key)):
            raise ValueError("ApiKeys not found in dummy account")
        return [(var, third_party_env_vars.get(var)) for var in env_vars]


def fetch_from_sdk(provider: BaseProviderModel) -> list[dict[str, Any]]:
    """
    Fetches the backends from the provider's SDK

    Returns:
    - list[dict]: A list of backends
    """
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

    return raw_output
