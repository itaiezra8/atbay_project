import string
import random

from ingest.utils.logger import logger

SCAN_ID_LENGTH = 12


def generate_scan_id() -> str:
    scan_id = ''.join(random.choices(string.ascii_letters+string.digits, k=SCAN_ID_LENGTH))
    logger.info(f'generated scan_id : {scan_id}')
    return scan_id
