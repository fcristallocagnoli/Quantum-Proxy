import datetime
from typing import Annotated, Optional
from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


PyObjectId = Annotated[str, BeforeValidator(str)]

Date = Annotated[datetime.datetime, BeforeValidator(str)]


class UserModel(BaseModel):
    # Asi, el campo id se valida y se serializa como "_id"
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    # Así, el campo id se valida como "_id" y se selializa como "id"
    # id: Optional[PyObjectId] = Field(
    #     validation_alias="_id", serialization_alias="id", default=None
    # )
    username: Optional[str] = Field(default=None)
    email: str = Field(...)
    password_hash: str = Field(...)
    api_keys: Optional[dict[str, str]] = Field(default=None)
    created_at: Optional[Date] = Field(default=None)
    model_config = ConfigDict(
        # Para permitir "User(id=...)", en vez de "User(_id=...)"
        populate_by_name=True,
        # Para poder incluir clases que no hereden de BaseModel como campos
        # es decir, que no se validen, solo chequea que sea del tipo correcto
        arbitrary_types_allowed=True,
    )


class UpdateUserModel(BaseModel):
    # Asi, el campo id se valida y se serializa como "_id"
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    # Así, el campo id se valida como "_id" y se selializa como "id"
    # id: Optional[PyObjectId] = Field(
    #     validation_alias="_id", serialization_alias="id", default=None
    # )
    username: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    api_keys: Optional[dict[str, str]] = None
    created_at: Optional[Date] = None
    model_config = ConfigDict(
        # Para poder incluir clases que no hereden de BaseModel como campos
        # es decir, que no se validen, solo chequea que sea del tipo correcto
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


UserDTO = type("UserDTO", (UpdateUserModel,), {})
