import datetime
from enum import StrEnum
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

Date = Annotated[datetime.datetime, BeforeValidator(str)]

class ClassType(StrEnum):
    IONQ = "IonQBackend"
    IBM = "IBMBackend"
    RIGETTI = "RigettiBackend"
    BRAKET = "AmazonBraketBackend"


class ProviderFK(BaseModel):
    provider_id: PyObjectId
    provider_name: str
    provider_from: Optional[str] = None


class BaseBackendModel(BaseModel):
    id: Optional[PyObjectId] = Field(
        validation_alias="_id", serialization_alias="id", default=None
    )
    provider: Optional[ProviderFK] = Field(default=None)
    backend_name: Optional[str] = Field(default=None)
    extra: Optional[list[str]] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
    last_checked: Optional[Date] = Field(default=None)


# --------------------------------------


class Queue(BaseModel):
    type: str
    value: str


class IonQBackend(BaseBackendModel):
    class_type: Literal[ClassType.IONQ] = Field(default=ClassType.IONQ, exclude=True)
    status: Optional[str] = Field(default=None)
    qubits: Optional[int] = Field(default=None)
    queue: Optional[Queue] = Field(default=None)
    last_updated: Optional[str] = Field(default=None)
    # may be processing jobs slower than usual
    degraded: Optional[bool] = Field(default=None)
    # solo aparece usando token
    has_access: Optional[bool] = Field(default=None)
    # para el hardware real
    characterization: Optional[dict] = Field(default=None)
    # Para los simuladores
    noise_models: Optional[list[str]] = Field(default=None)
    # campos que incluye IonQ
    extra: Optional[list[str]] = Field(default=None)


# --------------------------------------


class IBMBackend(BaseBackendModel):
    class_type: Literal[ClassType.IBM] = Field(default=ClassType.IBM, exclude=True)
    status: Optional[str] = Field(default=None)
    qubits: Optional[int] = Field(default=None)
    queue: Optional[Queue] = Field(default=None)
    last_updated: Optional[str] = Field(default=None)
    basis_gates: Optional[list[str]] = Field(default=None)
    clops_h: Optional[int] = Field(default=None)
    credits_required: Optional[bool] = Field(default=None)
    max_experiments: Optional[int] = Field(default=None)
    max_shots: Optional[int] = Field(default=None)
    extra: Optional[list[str]] = Field(default=None)


# --------------------------------------


class RigettiBackend(BaseBackendModel):
    class_type: Literal[ClassType.RIGETTI] = Field(
        default=ClassType.RIGETTI, exclude=True
    )
    qubits: Optional[int] = Field(default=None)
    rep_rate: Optional[str] = Field(default=None)
    median_t1: Optional[str] = Field(default=None)
    median_t2: Optional[str] = Field(default=None)
    median_sim_1q_fidelity: Optional[str] = Field(default=None)
    median_2q_xy_fidelity: Optional[str] = Field(default=None)
    median_2q_cz_fidelity: Optional[str] = Field(default=None)
    median_ro_fidelity: Optional[str] = Field(default=None)
    median_active_reset_fidelity: Optional[str] = Field(default=None)
    extra: Optional[list[str]] = Field(default=None)


# --------------------------------------


class ShotsRange(BaseModel):
    min: int
    max: int


class DeviceCost(BaseModel):
    price: float
    unit: str


class AmazonBraketBackend(BaseBackendModel):
    class_type: Literal[ClassType.BRAKET] = Field(
        default=ClassType.BRAKET, exclude=True
    )
    status: Optional[str] = Field(default=None)
    qubits: Optional[int] = Field(default=None)
    queue: Optional[Queue] = Field(default=None)
    gates_supported: Optional[list[str]] = Field(default=None)
    shots_range: Optional[ShotsRange] = Field(default=None)
    device_cost: Optional[DeviceCost] = Field(default=None)
    extra: Optional[list[str]] = Field(default=None)


# --------------------------------------


BackendType = IonQBackend | IBMBackend | RigettiBackend | AmazonBraketBackend


class Backend(BaseModel):
    backend: BackendType = Field(discriminator="class_type")


def retrieve_backend(backend: Backend, as_dict=False):
    real_backend = backend.backend
    if as_dict:
        return real_backend.model_dump(exclude_none=True)
    return real_backend
