"""
### V1.0: Quantum Simulators not reacheable. Hopefully, prices are not intended to change.

Codigo para obtener los precios de los sistemas cuanticos y simuladores de la pagina de AWS Braket.
- ``get_system_pricing``: Obtiene los precios de los sistemas cuanticos
- ``get_simulator_pricing``: Obtiene los precios de los simuladores cuanticos
"""

from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.common.by import By

from utils.email_utils import send_error_mail


@contextmanager
def innit_driver(url: str):
    driver: webdriver.Chrome = None
    """Context manager para inicializar y cerrar el webdriver de Chrome."""
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Para ejecutar en modo sin ventana
        print("Iniciando webdriver...")
        driver = webdriver.Chrome(options=options)

        driver.get(url)
        driver.implicitly_wait(10)

        yield driver
    except:
        yield None
    finally:
        print("Cerrando webdriver...")
        if driver:
            driver.quit()


def get_system_pricing() -> list:
    quantum_computers = []
    with innit_driver("https://aws.amazon.com/es/braket/pricing/") as driver:
        table = driver.find_element(
            By.XPATH,
            '//*[@id="aws-element-949823fd-c56b-46d8-8955-a6919fa6ee28-panel-1"]/div/div[2]/table',
        )
        rows = table.find_elements(By.TAG_NAME, "tr")
        # ignoramos la fila de encabezados
        for row in rows[1:]:
            fila = row.find_elements(By.TAG_NAME, "td")
            hardware_provider, qpu_family = fila[0].text, fila[1].text
            per_task_price = float(fila[2].text.split()[0].replace(",", "."))
            per_shot_price = float(fila[3].text.split()[0].replace(",", "."))
            quantum_computers.append(
                {
                    "hardware_provider": hardware_provider,
                    "qpu_family": qpu_family,
                    "price": {
                        "full_price": f"${str(per_task_price)}/task + ${str(per_shot_price)}/shot",
                        "per_task_price": per_task_price,
                        "per_shot_price": per_shot_price,
                    },
                }
            )
    return quantum_computers


def get_simulator_pricing() -> list:
    quantum_circuit_simulators = [
        {
            "qpu_family": "DM1",
            "price": {"full_price": "$0.075/minute", "per_minute_price": 0.075},
        },
        {
            "qpu_family": "SV1",
            "price": {"full_price": "$0.075/minute", "per_minute_price": 0.075},
        },
        {
            "qpu_family": "TN1",
            "price": {"full_price": "$0.075/minute", "per_minute_price": 0.075},
        },
    ]
    return quantum_circuit_simulators


PRECIOS = []

def get_pricing() -> list:
    global PRECIOS
    if not PRECIOS:
        try:
            PRECIOS = get_system_pricing() + get_simulator_pricing()
        except Exception as e:
            print(f"Error al obtener los precios de AWS Braket: {e}")
            send_error_mail(e, "Error al obtener los precios de AWS Braket.")

    return PRECIOS


def main():
    print(get_pricing())


if __name__ == "__main__":
    main()
