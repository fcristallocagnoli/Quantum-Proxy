from enum import StrEnum
from typing import Annotated, Any, Literal, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class ProviderName(StrEnum):
    IONQ = "IonQ"
    IBM = "IBM Quantum"
    RIGETTI = "Rigetti"


class ThirdPartyEnum(StrEnum):
    AWS = "Amazon Braket"
    AZURE = "Azure Quantum"


class ThirdPartyKey(BaseModel):
    third_party_id: Optional[PyObjectId] = None
    third_party_name: ThirdPartyEnum


class Module(BaseModel):
    description: Optional[str] = None
    module_file: str
    func_to_eval: str


class ScraperRequest(BaseModel):
    fetch_method: Literal["WEB-SCRAPING"] = "WEB-SCRAPING"
    base_url: str
    # auth: Optional[dict[str, Any]] = None
    module: Module


class APIRequest(BaseModel):
    fetch_method: Literal["API"] = "API"
    base_url: str
    auth: Optional[dict[str, str]] = None
    module: Module


class SDKRequest(BaseModel):
    fetch_method: Literal["SDK"] = "SDK"
    auth: Optional[dict[str, list]] = None
    third_party: Optional[ThirdPartyEnum] = None
    module: Module


RequestTypes = APIRequest | SDKRequest | ScraperRequest


class BaseProviderModel(BaseModel):
    """
    Modelo base para los proveedores de servicios cuánticos.

    Fields (the ones required):
    - No fields are required ;)
    """

    # Así, el campo id se valida como "_id" y se selializa como "id"
    id: Optional[PyObjectId] = Field(
        validation_alias="_id", serialization_alias="id", default=None
    )
    name: Optional[str] = Field(default=None)
    pid: Optional[str] = Field(default=None)
    description: Optional[Any] = Field(default=None)
    url: Optional[str] = Field(default=None)
    from_third_party: Optional[bool] = Field(default=None)
    third_party: Optional[ThirdPartyKey] = Field(default=None)

    backend_request: Optional[RequestTypes] = Field(
        default=None,
        discriminator="fetch_method",
    )

    backends_ids: Optional[list[PyObjectId]] = Field(default=None)

    last_updated_at: Optional[str] = None
    model_config = ConfigDict(
        # Para permitir "Class(id=...)", en vez de "Class(_id=...)"
        populate_by_name=True,
        # Para poder incluir clases que no hereden de BaseModel como campos
        # es decir, que no se validen, solo chequea que sea del tipo correcto
        arbitrary_types_allowed=True,
    )
