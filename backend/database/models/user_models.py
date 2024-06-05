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
    first_name: Optional[str] = Field(validation_alias="firstName", default=None)
    last_name: Optional[str] = Field(validation_alias="lastName", default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)
    roles: Optional[list[str]] = Field(default=[])
    api_keys: Optional[dict[str, dict]] = Field(default=None)
    created_at: Optional[Date] = Field(default=None)
    disabled: Optional[bool] = Field(default=False)
    model_config = ConfigDict(
        # Para permitir "User(id=...)", en vez de "User(_id=...)"
        populate_by_name=True,
        # Para poder incluir clases que no hereden de BaseModel como campos
        # es decir, que no se validen, solo chequea que sea del tipo correcto
        arbitrary_types_allowed=True,
    )


class UserInDBModel(UserModel):
    verification_token: Optional[float] = Field(default=None)
    is_verified: Optional[bool] = Field(default=False)
    refresh_tokens: Optional[list[float]] = Field(default=[])
    reset_token: Optional[float] = Field(default=None)
    reset_token_expires: Optional[Date] = Field(default=None)
