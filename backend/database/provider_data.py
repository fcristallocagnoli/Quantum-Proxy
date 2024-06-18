import textwrap
from braket.aws import AwsDevice
from dotenv import load_dotenv

from database.models.providers_models import ThirdPartyEnum
from utils.utils import norm_str

load_dotenv()

providers_api_data = [
    {
        "name": "IonQ",
        "pid": "native.ionq",
        "description": "",
        "website": "https://ionq.com/",
        "wiki_name": "IonQ",
        "from_third_party": False,
        "backend_request": {
            "fetch_method": "API",
            "base_url": "http://api.ionq.co/v0.3",
            "auth": {
                "Authorization": "apiKey TOKEN",
            },
            "third_party": None,
            "module": {
                "func_to_eval": "get_backends",
                "module_file": "ionq_api_code",
            },
        },
        "backends_ids": [],
    },
    {
        "name": "IBM Quantum",
        "pid": "native.ibm_quantum",
        "description": textwrap.dedent(
            """
            <p>Check the <a href="https://quantum.ibm.com/services/resources" target="_blank">IBM Quantum Platform</a> for more information about systems.</p>
            """
        ),
        "website": "https://www.ibm.com/quantum",
        "wiki_name": "IBM Quantum Platform",
        "from_third_party": False,
        "backend_request": {
            "fetch_method": "API",
            "base_url": "https://api.quantum-computing.ibm.com/runtime",
            "auth": {
                "Authorization": "Bearer TOKEN",
            },
            "module": {
                "func_to_eval": "get_backends",
                "module_file": "ibm_api_code",
            },
        },
        "backends_ids": [],
    },
]

providers_ws_data = [
    {
        "name": "Rigetti",
        "pid": "native.rigetti",
        "description": "",
        "website": "https://www.rigetti.com/",
        "wiki_name": "Rigetti Computing",
        "from_third_party": False,
        "backend_request": {
            "fetch_method": "WEB-SCRAPING",
            "base_url": "https://qcs.rigetti.com/qpus",
            "module": {
                "func_to_eval": "get_backends",
                "module_file": "rigetti_ws_code_v2",
            },
        },
        "backends_ids": [],
    },
]

providers_sdk_data = [
    {
        "name": "Amazon Braket",
        "pid": "native.aws",
        "description": textwrap.dedent(
            """
            <p>
                <a href="https://aws.amazon.com/es/braket/" target="_blank">Amazon Braket</a> is a fully managed service for quantum computing in the cloud.
                You can either run your algorithms within a simulator or on real quantum computing hardware called Quantum Processing Unit (QPU).
                Programming will be done using the Python-based <a href="https://github.com/amazon-braket/amazon-braket-sdk-python" target="_blank">Amazon Braket SDK</a>
            """
        ),
        "website": "https://aws.amazon.com/braket/",
        "wiki_name": "",
        "from_third_party": False,
        "backend_request": {
            "fetch_method": "SDK",
            "auth": {
                "env_vars": [
                    "AWS_ACCESS_KEY_ID",
                    "AWS_SECRET_ACCESS_KEY",
                    "AWS_REGION",
                ]
            },
            "module": {
                "func_to_eval": "get_backends",
                "module_file": "braket_sdk_code",
            },
        },
        "backends_ids": [],
    },
]


def get_braket_providers():
    output = []
    devices = AwsDevice.get_devices()
    providers = []
    for device in devices:
        if device.provider_name in providers:
            continue
        providers.append(device.provider_name)
        template = {
            "name": device.provider_name,
            "pid": f"{norm_str(ThirdPartyEnum.AWS)}.{norm_str(device.provider_name)}",
            "description": "",
            "website": None,
            "wiki_name": "",
            "from_third_party": True,
            "third_party": {
                "third_party_id": None,
                "third_party_name": ThirdPartyEnum.AWS,
            },
            "backends_ids": [],
        }
        output.append(template)
    return output


# O se añaden a mano, o se puede recurrrir a la función anterior
# Nota: se necesita cargar el archivo .env con las credenciales de AWS
providers_data_from_braket = get_braket_providers()

providers_data = (
    providers_api_data
    + providers_ws_data
    + providers_sdk_data
    + providers_data_from_braket
)
