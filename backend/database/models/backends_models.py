from typing import Annotated, Any, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class ProviderFK(BaseModel):
    provider_id: PyObjectId
    provider_name: str


class BaseBackendModel(BaseModel):
    id: Optional[PyObjectId] = Field(
        validation_alias="_id", serialization_alias="id", default=None
    )
    provider: ProviderFK
    backend_name: str
    extra: Optional[list[str]] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


# --------------------------------------


class Queue:
    def __init__(self, queue_type: str, value: Any):
        self.type = queue_type
        self.value = value

    def __str__(self) -> str:
        return f"Queue({self.value}) = {self.type}"


class IonQBackend(BaseBackendModel):
    status: str
    qubits: int
    queue: Queue
    last_updated: str
    # may be processing jobs slower than usual
    degraded: bool
    # solo aparece usando token
    has_access: Optional[bool] = None
    # para el hardware real
    characterization: Optional[str] = None
    # Para los simuladores
    noise_models: Optional[list[str]] = None
    # campos que incluye IonQ
    extra: list[str]


# --------------------------------------


class IBMBackend(BaseBackendModel):
    status: str
    qubits: int
    queue: Queue
    last_updated: str
    basis_gates: list[str]
    clops_h: int
    credits_required: bool
    max_experiments: int
    max_shots: int
    extra: list[str]


# --------------------------------------


class RigettiBackend(BaseBackendModel):
    qubits: int
    rep_rate: str
    median_t1: str
    median_t2: str
    median_sim_1q_fidelity: str
    median_2q_xy_fidelity: str
    median_2q_cz_fidelity: str
    median_ro_fidelity: str
    median_active_reset_fidelity: str
    extra: list[str]
