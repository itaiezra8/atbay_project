from flask import Flask, Response
from typing import Dict, Any
import threading

from core.utils.consts import POSTGRESQL_URI
from ingest.api.process_api import send_process_request
from ingest.utils.consts import SERVER_HOST, SERVER_PROT
from ingest.utils.generators import generate_scan_id
from ingest.utils.logger import logger


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_URI


@app.route('/ingest', methods=['POST'])
def ingest_handler() -> Dict[str, Any]:
    logger.debug('handling ingest request...')
    scan_id = generate_scan_id()
    threading.Thread(target=send_process_request, args=[scan_id]).start()
    # update status accepted
    return {
        'msg': 'request scanning received!',
        'scan_id': scan_id
    }


@app.errorhandler(404)
def default_handler(e):
    return Response(status=404)


if __name__ == '__main__':
    logger.debug('starting ingest server...')
    app.run(host=SERVER_HOST, port=SERVER_PROT, debug=True, threaded=True)
