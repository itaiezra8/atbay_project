import pika

from core.utils.helpers import is_valid_scan_id
from process.utils.consts import SERVER_HOST, SERVER_PORT
from process.utils.helpers import update_scan_in_db, execute_scan_process
from process.utils.logger import logger


logger.info('connecting to rabbit ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='scans', durable=True)
data = []


def process_handler(ch, method, properties, body):
    print(body.decode())
    scan_id = body.decode()
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
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='scans', on_message_callback=process_handler)
channel.start_consuming()
