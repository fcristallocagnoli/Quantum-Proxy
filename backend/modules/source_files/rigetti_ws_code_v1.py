"""
### V1.0: Multiple QPUs available in Rigetti's page

Codigo para obtener la informacion de los QPUs de Rigetti
- ``get_qpu_name``: Obtiene el nombre de la QPU en la pagina actual
- ``get_properties``: Obtiene las propiedades de la QPU en la pagina actual
- ``find_qpu_buttons``: Encuentra los botones de las QPUs disponibles
- ``get_page_info``: Obtiene la informacion de la pagina
- ``get_descriptions``: Obtiene las descripciones de los backends (para almacenar en el proveedor)
- ``get_backends``: Reune la informacion de todos los backends
"""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.relative_locator import locate_with

from modules.scraper_module import innit_driver


def get_qpu_name(driver: webdriver.Chrome) -> str:
    return driver.find_element(By.TAG_NAME, "h2").text.split()[0]


def get_properties(driver: webdriver.Chrome) -> tuple[dict, dict]:
    system_props, performance_snapshot = driver.find_element(
        By.XPATH, '//*[@id="app-layout"]/main/div/div/div[2]/div[2]'
    ).find_elements(By.TAG_NAME, "div")

    # System
    titulo_h3 = system_props.find_element(By.TAG_NAME, "h3").text
    system_props_dict = {titulo_h3: {}}
    for row in system_props.find_elements(By.TAG_NAME, "tr"):
        key, value = map(lambda f: f.text, row.find_elements(By.TAG_NAME, "td"))
        system_props_dict[titulo_h3].update({key: value})

    # Performance Snapshot
    titulo_h3 = performance_snapshot.find_element(By.TAG_NAME, "h3").text
    performance_dict = {titulo_h3: {}}
    for row in performance_snapshot.find_elements(By.TAG_NAME, "tr"):
        key, value = map(lambda f: f.text, row.find_elements(By.TAG_NAME, "td"))
        performance_dict[titulo_h3].update({key: value})

    return system_props_dict, performance_dict


def find_qpu_buttons(driver: webdriver.Chrome) -> list[WebElement]:
    try:
        locator = locate_with(
            By.XPATH, '//*[@id="app-layout"]/main/div/div/div[1]/div'
        ).near(driver.find_element(By.TAG_NAME, "h2"))
        div_qpus = driver.find_element(locator)

        return div_qpus.find_elements(By.TAG_NAME, "button")
    except Exception:
        return []


def get_page_info(driver: webdriver.Chrome) -> dict:
    """Get the information of the page"""
    sys_props, perf_props = get_properties(driver)
    return {
        "backend": get_qpu_name(driver),
        **sys_props,
        **perf_props,
    }


def get_backends(driver: webdriver.Chrome) -> list[dict]:
    output = [get_page_info(driver)]
    qpu_buttons: list = find_qpu_buttons(driver)
    element: WebElement
    for element in qpu_buttons[1:]:
        element.click()
        # Esperamos a que cargue la informaciÃ³n
        time.sleep(1)
        output.append(get_page_info(driver))
    # print(json.dumps(output, ensure_ascii=False))
    return output


def get_descriptions(driver: webdriver.Chrome) -> dict:
    description: dict[str, str | list] = {"provider": [], "backends": []}
    locator = locate_with(By.TAG_NAME, "p").above(
        driver.find_element(By.ID, "qpu_spec_charts")
    )

    first, *last = driver.find_elements(locator)[::-1]

    description.update({"provider": [first.text] + list(map(lambda e: e.text, last))})

    for button in find_qpu_buttons(driver):
        button.click()
        # Esperamos a que cargue la informaciÃ³n
        time.sleep(1)
        _, change, *_ = driver.find_elements(locator)[::-1]
        description["backends"].append(
            {"name": get_qpu_name(driver), "description": change.text}
        )

    # print(json.dumps({"descriptions": description}, ensure_ascii=False))
    return description

def main():
    with innit_driver("https://qcs.rigetti.com/qpus") as driver:
        backends: list = get_backends(driver)
        print(backends)

if __name__ == '__main__':
    main()