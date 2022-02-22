import requests
import time
import random
from typing import Dict

from core.utils.helpers import action_response
from core.utils.consts import POSTGRES_URL


def update_scan_in_db(path: str, scan_id: str) -> Dict[str, str]:
    try:
        response = requests.put(f'{POSTGRES_URL}/{path}', params={'scan_id': scan_id})
    except requests.exceptions.RequestException as err:
        return action_response('failure', str(err))
    return response.json()


def execute_scan_process() -> bool:
    time.sleep(10)
    return bool(random.getrandbits(1))
