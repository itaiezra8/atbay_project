import pika
import requests
import string
import random
from typing import Dict

from core.utils.helpers import action_response
from core.utils.consts import SCAN_ID_LENGTH, POSTGRES_URL
from ingest.utils.logger import logger


def generate_scan_id() -> str:
    scan_id = ''.join(random.choices(string.ascii_letters+string.digits, k=SCAN_ID_LENGTH))
    logger.info(f'generated scan_id : {scan_id}')
    return scan_id


def create_new_scan_in_db(scan_id: str) -> Dict[str, str]:
    try:
        response = requests.post(f'{POSTGRES_URL}/new_scan', json={'scan_id': scan_id})
    except requests.exceptions.RequestException as err:
        return action_response('failure', str(err))
    return response.json()


def publish_scan_to_rabbit(channel, connection, scan_id: str) -> None:
    channel.basic_publish(
        exchange='at-bay',
        routing_key='scans',
        body=scan_id,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()
