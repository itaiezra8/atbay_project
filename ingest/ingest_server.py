from flask import Flask
import asyncio

from ingest.utils.consts import SERVER_HOST, SERVER_PROT
from ingest.utils.logger import logger


app = Flask(__name__)


@app.route('/')
async def ingest_handler():
    return {'msg': 'Hello, World!'}


if __name__ == '__main__':
    logger.info('starting ingest server...')
    app.run(host=SERVER_HOST, port=SERVER_PROT, debug=True)
