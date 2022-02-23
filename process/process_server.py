import pika
import threading

from core.utils.consts import RABBIT_EXCHANGE, RABBIT_QUEUE
from core.utils.helpers import is_valid_scan_id
from process.utils.helpers import update_scan_in_db, execute_scan_process
from process.utils.logger import logger


def connect_to_rabbitmq():
    logger.info('connecting to rabbit ...')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=RABBIT_EXCHANGE, exchange_type='topic')
    channel.queue_declare(queue=RABBIT_QUEUE, durable=True)
    channel.queue_bind(exchange=RABBIT_EXCHANGE, queue=RABBIT_QUEUE, routing_key='#')
    return channel


def process_handler(ch, method, properties, body):
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


if __name__ == '__main__':
    channel = connect_to_rabbitmq()
    logger.info('start consuming rabbit...')
    channel.basic_consume(queue='scans', on_message_callback=process_handler)
    channel.start_consuming()
    # if we want to consume asynchronous
    # consumer_thread = threading.Thread(target=channel.start_consuming)
    # consumer_thread.start()
    # consumer_thread.join()
