from flask import Flask, Response
import pika
from typing import Dict
import threading

from core.utils.consts import POSTGRESQL_URI
from ingest.utils.consts import SERVER_HOST, SERVER_PORT
from ingest.utils.helpers import generate_scan_id, create_new_scan_in_db, publish_scan_to_rabbit
from ingest.utils.logger import logger


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_URI


def connect_to_rabbitmq() -> None:
    logger.info('connecting to rabbit ...')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='scans', durable=True)
    app.config['RABBITMQ_CONNECTION'] = connection
    app.config['RABBITMQ_CHANNEL'] = channel


@app.route('/ingest', methods=['POST'])
def ingest_handler() -> Dict[str, str]:
    logger.debug('handling ingest request...')
    scan_id = generate_scan_id()
    db_res = create_new_scan_in_db(scan_id)
    if db_res.get('status', '') != 'success':
        return {'msg': 'scanning request was not accepted!'}
    threading.Thread(target=publish_scan_to_rabbit, args=[app.config['RABBITMQ_CHANNEL'], app.config['RABBITMQ_CONNECTION'], scan_id]).start()
    return {
        'msg': 'scanning request accepted!',
        'scan_id': scan_id
    }


@app.errorhandler(404)
def default_handler(e):
    return Response(status=404)


if __name__ == '__main__':
    connect_to_rabbitmq()
    logger.debug('starting ingest server...')
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True, threaded=True)
