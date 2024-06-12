from database.models.providers_models import BaseProviderModel
from database.schemas.backend_schema import normalize_backend
from modules.api_module import fetch_from_api
from modules.scraper_module import fetch_from_ws
from modules.sdk_module import fetch_from_sdk


def fetch_data(provider: BaseProviderModel):
    request = provider.backend_request
    if not request:
        return None
    match request.fetch_method:
        case "API":
            data = fetch_from_api(provider)
        case "WEB-SCRAPING":
            data = fetch_from_ws(provider)
        case "SDK":
            data = fetch_from_sdk(provider)
        case _:
            return None
    return list(map(normalize_backend, data))
