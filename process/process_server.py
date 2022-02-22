from flask import Flask, request, Response

from process.utils.consts import SERVER_HOST, SERVER_PORT
from process.utils.logger import logger

app = Flask(__name__)


@app.route('/scan', methods=['POST'])
def process_handler():
    logger.debug(f'handling scan request...')
    data = request.get_json()
    if not data:
        logger.error('request body invalid!')
        return Response(status=400)
    scan_id = data.get('scan_id', '')
    if not scan_id:
        logger.error(f'did not received scan_id')
        return Response(status=400)
    # do some scanning work
    return Response(status=200)


@app.errorhandler(404)
def default_handler(e):
    return Response(status=404)


if __name__ == '__main__':
    logger.debug('starting process server...')
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True, threaded=False)
