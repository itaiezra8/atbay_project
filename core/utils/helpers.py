from typing import Dict

from core.utils.consts import SCAN_ID_LENGTH


def action_response(status: str, msg: str) -> Dict[str, str]:
    return {'status': status, 'msg': msg}


def is_valid_scan_id(scan_id: str) -> bool:
    return len(scan_id) == SCAN_ID_LENGTH
