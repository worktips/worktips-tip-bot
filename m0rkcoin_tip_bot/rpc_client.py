from typing import Dict
from uuid import uuid4

import requests

from m0rkcoin_tip_bot.config import config


def call_method(method_name: str, payload: Dict = None) -> Dict:
    full_payload = {
        'params': payload or {},
        'jsonrpc': '2.0',
        'id': str(uuid4()),
        'method': f'{method_name}'
    }
    resp = requests.post(
        f'http://{config.wallet.host}:{config.wallet.port}/json_rpc',
        json=full_payload)
    resp.raise_for_status()
    return resp.json().get('result', {})
