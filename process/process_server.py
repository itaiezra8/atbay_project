from flask import Flask, request, Response

from core.utils.helpers import is_valid_scan_id
from process.utils.consts import SERVER_HOST, SERVER_PORT
from process.utils.helpers import update_scan_in_db, execute_scan_process
from process.utils.logger import logger

app = Flask(__name__)


@app.route('/scan', methods=['POST'])
def process_handler() -> None:
    logger.debug(f'handling scan request...')
    data = request.get_json()
    if not data or type(data) != dict:
        logger.error('request body invalid!')
    scan_id = data.get('scan_id', '')

    if not is_valid_scan_id(scan_id):
        logger.info(f'scan_id: {scan_id} is not valid!')
    logger.info(f'start scanning scan_id: {scan_id}')
    update_scan_in_db('start_process', scan_id)
    scan_res = execute_scan_process()
    if not scan_res:
        logger.info(f'error found on scanning scan_id: {scan_id}')
        update_scan_in_db('error_process', scan_id)
    else:
        logger.info(f'finished scanning scan_id: {scan_id}')
        update_scan_in_db('end_process', scan_id)


@app.errorhandler(404)
def default_handler(e):
    return Response(status=404)


if __name__ == '__main__':
    logger.debug('starting process server...')
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True, threaded=False)
