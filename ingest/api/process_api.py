import requests
import time

PROCESS_URL = 'http://localhost:5020/scan'


def send_process_request(scan_id: str) -> None:
    try:
        requests.post(PROCESS_URL, json={'scan_id': scan_id})
    except requests.exceptions.RequestException as err:
        # send status error with err
        pass
