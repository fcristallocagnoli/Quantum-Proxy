# From DB to Provider (Any)
def provider_schema(provider: dict) -> dict:
    """
    Mapea un documento obtenido de la BD, a un diccionario tratable
    - Concretamente, elimina la clave '_id' si es que la tuviera
    """
    # Mapeamos el _id autogenerado de mongodb a id
    # y desempaquetamos el resto de los campos tal cual
    if "_id" in provider.keys():
        return {"id": str(provider.pop("_id")), **provider}
    else:
        return provider


def providers_schema(providers) -> list:
    """
    Mapea un iterable de documentos obtenidos de la BD, a diccionarios tratables
    - Concretamente, elimina la clave '_id' si es que la tuviera
    """
    return [provider_schema(provider) for provider in providers]
