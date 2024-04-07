from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class Scraper(BaseModel):
    description: str
    func_to_eval: str
    code_to_compile: str


class ScraperRequest(BaseModel):
    fetch_method: Literal["WEB-SCRAPING"] = "WEB-SCRAPING"
    base_url: str
    scraper: Scraper


class APIRequest(BaseModel):
    fetch_method: Literal["API"] = "API"
    base_url: str
    headers: Optional[dict[str, str]] = None
    params: Optional[dict[str, str]] = None


BackendRequest = APIRequest | ScraperRequest


class BaseProvider(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Any = None
    url: Optional[str] = None

    backend_request: Optional[APIRequest | ScraperRequest] = Field(
        default=None,
        discriminator="fetch_method",
    )

    last_checked: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
