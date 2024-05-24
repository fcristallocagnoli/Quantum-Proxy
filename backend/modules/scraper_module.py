import importlib.util
from contextlib import contextmanager
from pathlib import Path

from bson import ObjectId
from database.models.providers_models import BaseProviderModel
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from utils.email_utils import send_error_mail
from utils.utils import check_code


@contextmanager
def innit_driver(url: str):
    """Context manager para inicializar y cerrar el webdriver de Chrome."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Para ejecutar en modo sin ventana
        print("Iniciando webdriver...")
        driver = webdriver.Chrome(options=options)

        driver.get(url)
        driver.implicitly_wait(10)

        yield driver
    finally:
        print("Cerrando webdriver...")
        driver.quit()


def fetch_from_ws(provider: BaseProviderModel) -> list[dict]:
    """
    Fetch data from a website using web scraping.

    Returns:
    - list[dict]: A list of backends
    """
    print("Fetching from web scraping...")
    module = provider.backend_request.module
    func = module.func_to_eval
    file_name = module.module_file
    file_path = (
        Path(__file__).parent.joinpath("source_files").joinpath(f"{file_name}.py")
    )

    if not check_code(file_path):
        return []

    # Ejecutar el código en un contexto que proporciona un webdriver
    with innit_driver(provider.backend_request.base_url) as driver:
        # Importamos el módulo dinámicamente desde el archivo externo
        especificacion = importlib.util.spec_from_file_location(file_name, file_path)
        modulo = importlib.util.module_from_spec(especificacion)
        especificacion.loader.exec_module(modulo)

        raw_output: list[dict] = []
        try:
            # Ejecutamos la función designada y obtenemos los datos
            raw_output = getattr(modulo, func)(driver)
        except NoSuchElementException as error:
            print(f"Error al obtener los datos: {error.msg}")
            send_error_mail(error, "Error al obtener los datos via webscraping.")
        except Exception as error:
            print(f"Error inesperado: {error}")
            send_error_mail(error, "Error inesperado al obtener los datos via webscraping.")
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
