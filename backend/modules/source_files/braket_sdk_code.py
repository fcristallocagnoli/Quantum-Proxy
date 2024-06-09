import os
from typing import Any

from braket.aws import AwsDevice
from braket.aws.queue_information import QueueType
from braket.device_schema import DeviceActionType
from bson import ObjectId
from database.models.providers_models import SDKRequest, ThirdPartyEnum
from database.mongo_client import db_find_provider
from modules.sdk_module import get_env_vars_if_needed
from utils.utils import norm_str


def process_device(device: AwsDevice) -> dict[str, Any]:
    provider = db_find_provider(
        filter={
            "pid": f"{norm_str(ThirdPartyEnum.AWS)}.{norm_str(device.provider_name)}"
        }
    )

    # --------------------------------------
    supports_gates = device.properties.action.get(DeviceActionType.OPENQASM, None)
    return {
        "provider": {
            "provider_id": ObjectId(provider["_id"]),
            "provider_name": provider["name"],
            "provider_from": ThirdPartyEnum.AWS
        },
        "device_name": device.name,
        "status": device.status.lower(),
        "qubit_count": device.properties.paradigm.qubitCount,
        "queue_depth": device.queue_depth().quantum_tasks.get(QueueType.NORMAL, -1),
        "gates_supported": supports_gates.supportedOperations if supports_gates else [],
        "shots_range": {
            "min": device.properties.service.shotsRange[0],
            "max": device.properties.service.shotsRange[1],
        },
        "device_cost": {
            "price": device.properties.service.deviceCost.price,
            "unit": device.properties.service.deviceCost.unit,
        },
        # "execution_windows": device.properties.service.executionWindows,
    }


def get_backends(request: SDKRequest = None) -> list[dict[str, Any]]:
    key_value_list = get_env_vars_if_needed(request, provider_key="amazon_braket")

    for key, value in key_value_list:
        os.environ[key] = value

    output = []
    for device in AwsDevice.get_devices():
        output.append(process_device(device))
    return output
