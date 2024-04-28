import importlib.util
from contextlib import contextmanager
from pathlib import Path

from database.models.providers_models import BaseProviderModel
from database.mongo_client import db_find_provider
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from utils.email_utils import error_mail
from utils.utils import check_code, norm_id


@contextmanager
def innit_driver(url: str):
    """Context manager para inicializar y cerrar el webdriver de Chrome."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Para ejecutar en modo sin ventana
        print("Iniciando webdriver...")
        driver = webdriver.Chrome(options=options)

        print("Cargando página...")
        driver.get(url)
        driver.implicitly_wait(10)

        yield driver
    finally:
        print("Cerrando webdriver...")
        driver.quit()
        print("Webdriver cerrado.")


def fetch_from_ws(provider: BaseProviderModel) -> list[dict]:
    """
    Fetch data from a website using web scraping.

    Returns:
    - list[dict]: A list of backends
    """
    print("Fetching from web scraping...")
    func = provider.backend_request.module.func_to_eval
    file_name = provider.backend_request.module.module_file
    file_path = (
        Path(__file__).parent.joinpath("source_files").joinpath(f"{file_name}.py")
    )

    if not check_code(file_path):
        return []

    # Ejecutar el código en un contexto que proporciona un webdriver
    with innit_driver(provider.backend_request.base_url) as driver:
        # Cargar el módulo desde el archivo externo
        especificacion = importlib.util.spec_from_file_location(file_name, file_path)
        modulo = importlib.util.module_from_spec(especificacion)
        especificacion.loader.exec_module(modulo)

        # Llamar a la función del fragmento de código externo
        raw_output: list[dict] = []
        try:
            raw_output = getattr(modulo, func)(driver)
        except NoSuchElementException as error:
            print(f"Error al obtener los datos: {error.msg}")
            error_mail(error, "Error al obtener los datos via webscraping.")
        except Exception as error:
            print(f"Error inesperado: {error}")
            error_mail(error, "Error inesperado al obtener los datos via webscraping.")
        provider_data = {
            "provider_id": norm_id(db_find_provider(filter={"name": provider.name})),
            "provider_name": provider.name,
        }
        raw_output = list(
            map(
                lambda back: back.update({"provider": provider_data}) or back,
                raw_output,
            )
        )
    return raw_output
