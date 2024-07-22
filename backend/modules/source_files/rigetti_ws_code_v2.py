"""
### V2.0: Single QPU available in Rigetti's page
- Código adaptado de V1.0 para obtener la información cuando solo hay una QPU disponible

Codigo para obtener la informacion de los QPUs de Rigetti
- ``get_qpu_name``: Obtiene el nombre de la QPU en la pagina actual
- ``get_properties``: Obtiene las propiedades de la QPU en la pagina actual
- ``get_page_info``: Obtiene la informacion de la pagina
- ``get_descriptions``: Obtiene las descripciones del backend (para almacenar en el proveedor)
- ``get_backends``: Reune la informacion del backend
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

from modules.scraper_module import innit_driver


def get_qpu_name(driver: webdriver.Chrome) -> str:
    """Get the name of the QPU from the page title"""
    return driver.find_element(By.TAG_NAME, "h2").text.split()[0]


def get_properties(driver: webdriver.Chrome) -> tuple[dict, dict]:
    """Get the properties of the QPU from the page"""
    system_props, performance_snapshot = driver.find_element(
        By.XPATH, '//*[@id="app-layout"]/main/div/div/div[1]/div[2]'
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


def get_page_info(driver: webdriver.Chrome) -> dict:
    """Get the information of the page"""
    sys_props, perf_props = get_properties(driver)
    return {
        "backend": get_qpu_name(driver),
        **sys_props,
        **perf_props,
    }


def get_backends(driver: webdriver.Chrome) -> list[dict]:
    """
    Get the properties of the QPU in the page
    """
    output = [get_page_info(driver)]
    # print(json.dumps(output, ensure_ascii=False))
    return output


def get_descriptions(driver: webdriver.Chrome) -> dict:
    """
    ### #Outdated
    Get the descriptions of the QPU in the page
    """
    description: dict[str, str | list] = {"provider": [], "backends": []}
    locator = locate_with(By.TAG_NAME, "p").above(
        driver.find_element(By.ID, "qpu_spec_charts")
    )

    first, *last = driver.find_elements(locator)[::-1]

    description.update({"provider": [first.text] + list(map(lambda e: e.text, last))})

    _, change, *_ = driver.find_elements(locator)[::-1]
    description["backends"].append(
        {"name": get_qpu_name(driver), "description": change.text}
    )

    # print(json.dumps({"descriptions": description}, ensure_ascii=False))
    # return {"description": description}
    return description


def main():

    with innit_driver("https://qcs.rigetti.com/qpus") as driver:
        backends: list = get_backends(driver)
        print(backends)


if __name__ == "__main__":
    main()
