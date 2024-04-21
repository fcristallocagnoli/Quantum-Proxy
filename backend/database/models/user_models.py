import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


PyObjectId = Annotated[str, BeforeValidator(str)]

Date = Annotated[datetime.datetime, BeforeValidator(str)]


class UserModel(BaseModel):
    # Así, el campo id se valida como "_id" y se selializa como "id"
    id: Optional[PyObjectId] = Field(
        validation_alias="_id", serialization_alias="id", default=None
    )
    username: Optional[str] = Field(default=None)
    full_name: Optional[str] = Field(default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)
    roles: Optional[list[str]] = Field(default=[])
    api_keys: Optional[dict[str, str]] = Field(default=None)
    created_at: Optional[Date] = Field(default=None)
    disabled: Optional[bool] = Field(default=False)
    model_config = ConfigDict(
        # Para permitir "User(id=...)", en vez de "User(_id=...)"
        populate_by_name=True,
        # Para poder incluir clases que no hereden de BaseModel como campos
        # es decir, que no se validen, solo chequea que sea del tipo correcto
        arbitrary_types_allowed=True,
    )
