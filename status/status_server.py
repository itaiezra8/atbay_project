from flask import Flask, Response
from typing import Dict, Any


from status.utils.consts import SERVER_HOST, SERVER_PORT
from status.utils.logger import logger


app = Flask(__name__)


@app.route('/status', methods=['GET'])
def status_handler() -> Dict[str, Any]:
    # make get status req
    pass


@app.errorhandler(404)
def default_handler(e):
    return Response(status=404)


if __name__ == '__main__':
    logger.debug('starting status server...')
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True, threaded=True)