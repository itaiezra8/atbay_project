import requests
from typing import Dict

from core.utils.helpers import action_response
from core.utils.consts import POSTGRES_URL


def check_scan_status(scan_id: str) -> Dict[str, str]:
    try:
        response = requests.get(f'{POSTGRES_URL}/status', params={'scan_id': scan_id})
    except requests.exceptions.RequestException as err:
        return action_response('failure', str(err))
    return response.json()
