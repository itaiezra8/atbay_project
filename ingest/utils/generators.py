import string
import random

from core.utils.consts import SCAN_ID_LENGTH
from ingest.utils.logger import logger


def generate_scan_id() -> str:
    scan_id = ''.join(random.choices(string.ascii_letters+string.digits, k=SCAN_ID_LENGTH))
    logger.info(f'generated scan_id : {scan_id}')
    return scan_id
