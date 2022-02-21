import time

from flask import Flask, request
from flask_migrate import Migrate
from postgresql.cyber_scans import db, ScansModel
from postgresql.utils.consts import SERVER_HOST, SERVER_PROT, POSTGRESQL_URI

from postgresql.utils.logger import logger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        logger.error('request body invalid!')
    scan_id = data.get('scan_id', '')
    new_scan = ScansModel(scan_id=scan_id, scan_req_time=time.time(), status='accepted')
    db.session.add(new_scan)
    db.session.commit()
    return f"Done!!"


if __name__ == '__main__':
    logger.debug('starting ingest server...')
    app.run(host=SERVER_HOST, port=SERVER_PROT, debug=True)
