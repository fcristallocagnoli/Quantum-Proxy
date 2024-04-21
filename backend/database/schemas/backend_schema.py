from database.models.providers_models import ProviderName
from utils.utils import convert_from_ms, from_seconds_to_date, fromisoformat


def normalize_backend(backend: dict):
    """Normalize backend data depending on the provider"""
    print(backend)
    match name := backend["provider"]["provider_name"]:
        case ProviderName.IONQ:
            return ionq_normalizer(backend)
        case ProviderName.IBM:
            return ibm_normalizer(backend)
        case ProviderName.RIGETTI:
            return rigetti_normalizer(backend)
        case _:
            return norm_error(name)


def ionq_normalizer(backend: dict) -> dict:
    """Normalize IonQ backend data"""
    is_simulator: bool = backend["backend"] == "simulator"
    norm_back = {
        "provider": backend["provider"],
        "backend_name": backend["backend"],
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
        "provider": backend["provider"],
        "backend_name": backend["backend"],
        # --------------------------------------
        "status": backend["status"],
        "qubits": backend["qubits"],
        "queue": {
            "type": "jobs_remaining",
            "value": backend["queue"],
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

def norm_error(name: str):
    """Raise an error if the provider is not supported"""
    raise ValueError(f"Backend {name} not supported")