import requests
import time

PROCESS_URL = 'http://localhost:5020/scan'


def send_process_request(scan_id: str) -> None:
    try:
        time.sleep(10)
        print(f'yesssssss: {scan_id}')
        # requests.post(PROCESS_URL, data={'scan_id': scan_id})
    except requests.exceptions.RequestException as err:
        # send status error with err
        pass
