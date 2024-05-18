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
    module: Module


class APIRequest(BaseModel):
    fetch_method: Literal["API"] = "API"
    base_url: str
    auth: Optional[dict[str, str]] = None
    module: Module


class SDKRequest(BaseModel):
    fetch_method: Literal["SDK"] = "SDK"
    auth: Optional[dict[str, list]] = None
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
    description: Optional[Any] = Field(default="")
    url: Optional[str] = Field(default=None)
    from_third_party: Optional[bool] = Field(default=None)
    # --------------------------------------------------------------
    third_party: Optional[ThirdPartyKey] = Field(default=None)

    backend_request: Optional[RequestTypes] = Field(
        default=None,
        discriminator="fetch_method",
    )

    backends_ids: Optional[list[PyObjectId]] = Field(default=None)
    # --------------------------------------------------------------
    last_updated_at: Optional[str] = None
    model_config = ConfigDict(
        # Para permitir "Class(id=...)", en vez de "Class(_id=...)"
        populate_by_name=True,
        # Para poder incluir clases que no hereden de BaseModel como campos
        # es decir, que no se validen, solo chequea que sea del tipo correcto
        arbitrary_types_allowed=True,
    )


# XXX: Concepto de pruebas TODO - Implementar si es conveniente
# XXX: Borar si no se llega a implementar o usar
class NativeProviderModel(BaseProviderModel):
    """
    Modelo para los proveedores de servicios cuánticos nativos.
    """

    class_type: Literal["NativeProvider"] = "NativeProvider"
    backend_request: Optional[RequestTypes] = Field(
        default=None,
        discriminator="fetch_method",
    )
    backends_ids: Optional[list[PyObjectId]] = Field(default=None)


class ThirdPartyModel(BaseProviderModel):
    """
    Modelo para los servicios cuánticos de terceros.
    """

    class_type: Literal["ThirdParty"] = "ThirdParty"
    provided_providers: Optional[list[PyObjectId]] = Field(default=None)
    backends_ids: Optional[list[PyObjectId]] = Field(default=None)


class ThirdPartyProviderModel(BaseProviderModel):
    """
    Modelo para los proveedores ofrecidos por servicios cuánticos de terceros.
    """

    class_type: Literal["ThirdPartyProvider"] = "ThirdPartyProvider"
    third_party: ThirdPartyKey
    backends_ids: Optional[list[PyObjectId]] = Field(default=None)


ProviderType = NativeProviderModel | ThirdPartyModel | ThirdPartyProviderModel


class Provider(BaseModel):
    provider: ProviderType = Field(discriminator="class_type")


def crear_proveedor(provider: Provider):
    return provider.provider


# XXX: Concept
class IonQProvider(BaseProviderModel):

    def build_backends(self) -> dict[str, Any]: ...


class IBMProvider(BaseProviderModel):

    def build_backends(self) -> dict[str, Any]: ...


class RigettiProvider(BaseProviderModel):

    def build_backends(self) -> dict[str, Any]: ...


# Pruebas varias
def main():
    ...
    provider = Provider(
        provider=NativeProviderModel(
            name="IonQ",
            pid="ionq",
            description="IonQ is a quantum computing company that builds quantum computers for commercial applications.",
            url="https://ionq.com/",
            backend_request=APIRequest(
                base_url="https://ionq.com/",
                auth={"Authorization": "apiKey TOKEN"},
                module=Module(
                    description="Module to fetch the backends from IonQ",
                    module_file="ionq_api_code",
                    func_to_eval="get_backends",
                ),
            ),
            backends_ids=[],
        )
    )
    print("Provider tal cual:", provider)
    print("Provider creado:", crear_proveedor(provider))
    print("Provider creado:", type("ProviderReal", (), provider.provider.model_dump()))


if __name__ == "__main__":
    main()
