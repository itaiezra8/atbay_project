from flask import Flask, Response, request
from typing import Dict, Any

from status.utils.consts import SERVER_HOST, SERVER_PORT
from status.utils.helpers import check_scan_status
from status.utils.logger import logger


app = Flask(__name__)


@app.route('/status', methods=['GET'])
def status_handler() -> Dict[str, Any]:
    scan_id = request.args.get('scan_id', '')
    logger.debug(f'checking status for scan_id: {scan_id}')
    db_res = check_scan_status(scan_id)
    logger.info(f'{db_res.get("msg", "")}')
    return {'msg': db_res.get('msg', '')}


@app.errorhandler(404)
def default_handler(e):
    return Response(status=404)


if __name__ == '__main__':
    logger.debug('starting status server...')
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True, threaded=True)