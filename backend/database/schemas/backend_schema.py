from database.models.backends_models import ClassType
from database.mongo_client import db_find_provider
from database.models.providers_models import ProviderName, ThirdPartyEnum
from utils.utils import convert_from_ms, create_bid, from_seconds_to_date, fromisoformat, get_current_time_iso


def normalize_backend(backend: dict):
    """Normalize backend data depending on the provider"""
    provider = db_find_provider(
        filter={"_id": backend["provider"]["provider_id"]},
        projection={"from_third_party": 1, "third_party": 1}
    )
    if provider["from_third_party"]:
        match party_name := provider["third_party"]["third_party_name"]:
            case ThirdPartyEnum.AWS:
                norm_back = braket_normalizer(backend)
            case _:
                return norm_error(party_name)
    else:
        match name := backend["provider"]["provider_name"]:
            case ProviderName.IONQ:
                norm_back = ionq_normalizer(backend)
            case ProviderName.IBM:
                norm_back = ibm_normalizer(backend)
            case ProviderName.RIGETTI:
                norm_back = rigetti_normalizer(backend)
            case _:
                return norm_error(name)
    norm_back.update({
        "bid": create_bid(norm_back),
        "last_checked": get_current_time_iso()
    })
    return norm_back


def ionq_normalizer(backend: dict) -> dict:
    """Normalize IonQ backend data"""
    is_simulator: bool = backend["backend"] == "simulator"
    norm_back = {
        "class_type": ClassType.IONQ,
        "provider": backend["provider"],
        "backend_name": str(backend["backend"]).removeprefix("qpu.").capitalize(),
        # --------------------------------------
        "status": backend["status"],
        "qubits": backend["qubits"],
        "queue": {
            "type": "avg_time",
            "value": convert_from_ms(backend["average_queue_time"]),
        },
        "last_updated": from_seconds_to_date(backend["last_updated"]),
        "degraded": backend["degraded"],
        "has_access": backend["has_access"],
    }
    extra_values: list = [
        "status", "qubits", "queue", "last_updated", "degraded", "has_access"
    ]
    if is_simulator:
        norm_back.update({
            "noise_models": backend["noise_models"],
            "extra": extra_values + ["noise_models"]
        })
    else:
        norm_back.update({
            "characterization": backend["extra"]["characterization"],
            "extra": extra_values + ["characterization"]
        })
    return norm_back

def ibm_normalizer(backend: dict):
    """Normalize IBM backend data"""
    extra: dict = backend["extra"]
    norm_back = {
        "class_type": ClassType.IBM,
        "provider": backend["provider"],
        "backend_name": str(backend["backend"]).removeprefix("ibm_").capitalize(),
        # --------------------------------------
        "status": backend["status"],
        "qubits": backend["qubits"],
        "queue": {
            "type": "jobs_remaining",
            "value": str(backend["queue"]),
        },
        "last_updated": fromisoformat(backend["last_updated"]),
        "basis_gates": extra["basis_gates"],
        "clops_h": extra["clops_h"],
        "credits_required": extra["credits_required"],
        "max_experiments": extra["max_experiments"],
        "max_shots": extra["max_shots"],
        "extra": [
            "status", "qubits", "queue",
            "last_updated", "basis_gates", "clops_h",
            "credits_required", "max_experiments", "max_shots"
        ]
    }
    return norm_back


def rigetti_normalizer(backend: dict):
    """Normalize Rigetti backend data"""
    system, performance = backend["System"], backend["Performance Snapshot"]
    return {
        "class_type": ClassType.RIGETTI,
        "provider": backend["provider"],
        "backend_name": backend["backend"],
        # --------------------------------------
        "qubits": int(system["Qubits on device"]),
        "rep_rate": system["Rep rate"],
        "median_t1": performance["Median T1"],
        "median_t2": performance["Median T2"],
        "median_sim_1q_fidelity": performance["Median Sim 1Q Fidelity"],
        "median_2q_xy_fidelity": performance["Median 2Q XY Fidelity"],
        "median_2q_cz_fidelity": performance["Median 2Q CZ Fidelity"],
        "median_ro_fidelity": performance["Median RO Fidelity"],
        "median_active_reset_fidelity": performance["Median RO Fidelity"],
        "extra": [
            "qubits", "median_rep_rate",
            "median_t1", "median_t2", "median_sim_1q_fidelity",
            "median_2q_xy_fidelity", "median_2q_cz_fidelity",
            "median_ro_fidelity", "median_active_reset_fidelity"
        ]
    }

def braket_normalizer(backend: dict):
    """Normalize Braket backend data"""
    return {
        "class_type": ClassType.BRAKET,
        "provider": backend["provider"],
        "backend_name": backend["device_name"],
        # --------------------------------------
        "status": backend["status"],
        "qubits": backend["qubit_count"],
        "queue": {
            "type": "jobs_remaining",
            "value": backend["queue_depth"],
        },
        "gates_supported": backend["gates_supported"],
        "shots_range": backend["shots_range"],
        "device_cost": backend["device_cost"],
        "extra": [
            "status", "qubits", "queue", "gates_supported", "shots_range", "device_cost"
        ]
    }


def norm_error(name: str):
    """Raise an error if the provider is not supported"""
    raise ValueError(f"Backend {name} not supported")
