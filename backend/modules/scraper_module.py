import ast
import importlib.util
import os
from contextlib import contextmanager

from database.models.providers_models import ScraperRequest
from selenium import webdriver

SCRAPER_FILE = "code_to_compile.py"
SCRAPER_MODULE = SCRAPER_FILE.split(".")[0]


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


@contextmanager
def temp_file_manager(code: str):
    """Context manager para escribir y leer un archivo temporal."""
    try:
        with open(SCRAPER_FILE, "w") as f:
            f.write(code)
        yield
    finally:
        print("Borrando archivo temporal...")
        os.remove(SCRAPER_FILE)
        print("Archivo temporal borrado.")


def parse_code(code: str):
    """
    Validar el código antes de ejecutarlo.
    - Evitar llamadas a funciones peligrosas como eval() o exec().
    """
    arbol = ast.parse(code)

    # Recorrer el árbol y realizar operaciones de validación
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name):
            # Verificar si hay llamadas a funciones peligrosas
            if nodo.func.id in ["eval", "exec"]:
                raise ValueError(
                    "El código no puede contener llamadas a funciones peligrosas como eval() o exec()"
                )


def fetch_from_ws(request: ScraperRequest) -> list[dict]:
    print("Fetching from web scraping...")
    func = request.scraper.func_to_eval
    code = request.scraper.code_to_compile
    try:
        parse_code(code)
    except Exception as e:
        error = {
            SyntaxError.__name__: "Error de sintaxis en el código",
            ValueError.__name__: "Error al validar el código",
        }.get(type(e).__name__, "Error al ejecutar el código")
        print(error)
        raise

    with temp_file_manager(code):
        # Ejecutar el código en un contexto que proporciona un webdriver
        with innit_driver(request.base_url) as driver:
            # Cargar el módulo desde el archivo externo
            especificacion = importlib.util.spec_from_file_location(
                SCRAPER_MODULE, SCRAPER_FILE
            )
            modulo = importlib.util.module_from_spec(especificacion)
            especificacion.loader.exec_module(modulo)

            # Llamar a la función del fragmento de código externo
            raw_output: list[dict] = getattr(modulo, func)(driver)
    return raw_output
