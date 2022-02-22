from datetime import datetime, timedelta
from typing import Dict
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from core.utils.helpers import action_response, is_valid_scan_id
from postgresql.utils.consts import SERVER_HOST, SERVER_PORT, POSTGRESQL_URI
from postgresql.utils.logger import logger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRESQL_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ScansModel(db.Model):
    __tablename__ = 'cyber_scans'
    scan_id = db.Column(db.String(), primary_key=True)
    scan_req_time = db.Column(db.DateTime)
    start_scanning_process_time = db.Column(db.DateTime)
    finish_scanning_process_time = db.Column(db.DateTime)
    status = db.Column(db.String())

    def __init__(self, scan_id, scan_req_time, status):
        self.scan_id = scan_id
        self.scan_req_time = scan_req_time
        self.status = status


db.create_all()
db.session.commit()


@app.route('/new_scan', methods=['POST'])
def add_scan() -> Dict[str, str]:
    data = request.get_json()
    if not data or type(data) != dict:
        msg = 'request body invalid!'
        logger.error(msg)
        return action_response('failure', msg)
    scan_id = data.get('scan_id', '')
    if not is_valid_scan_id(scan_id):
        msg = f'scan_id: {scan_id} is not valid!'
        logger.info(msg)
        return action_response('failure', msg)
    scan = ScansModel(scan_id=scan_id, scan_req_time=datetime.now(), status='accepted')
    try:
        db.session.add(scan)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        msg = f'{scan_id} already exists!'
        logger.info(msg)
        return action_response('failure', msg)
    return action_response('success', 'scan added successfully!')


@app.route('/start_process', methods=['PUT'])
def start_scan_process() -> Dict[str, str]:
    scan_id = request.args.get('scan_id', '')
    scan = ScansModel.query.filter_by(scan_id=scan_id).first()
    if not scan:
        msg = f'scan_id: {scan_id} not exists!'
        logger.info(msg)
        return action_response('failure', msg)
    scan.start_scanning_process_time = datetime.now()
    scan.status = 'running'
    db.session.commit()
    logger.info(f'scan process of scan_id: {scan_id} has started')
    return action_response('success', 'updated scan start process successfully!')


@app.route('/end_process', methods=['PUT'])
def end_scan_process() -> Dict[str, str]:
    scan_id = request.args.get('scan_id', '')
    scan = ScansModel.query.filter_by(scan_id=scan_id).first()
    if not scan:
        msg = f'scan_id: {scan_id} not exists!'
        logger.info(msg)
        return action_response('failure', msg)
    scan.finish_scanning_process_time = datetime.now()
    scan.status = 'complete'
    db.session.commit()
    logger.info(f'scan process of scan_id: {scan_id} has completed')
    return action_response('success', 'updated scan finish process successfully!')


@app.route('/error_process', methods=['PUT'])
def error_scan_process() -> Dict[str, str]:
    scan_id = request.args.get('scan_id', '')
    scan = ScansModel.query.filter_by(scan_id=scan_id).first()
    if not scan:
        msg = f'scan_id: {scan_id} not exists!'
        logger.info(msg)
        return action_response('failure', msg)
    scan.finish_scanning_process_time = datetime.now()
    scan.status = 'error'
    db.session.commit()
    logger.info(f'scan process of scan_id: {scan_id} found with error')
    return action_response('success', 'updated error in scan process successfully!')


@app.route('/status', methods=['GET'])
def status_scan_process() -> Dict[str, str]:
    scan_id = request.args.get('scan_id', '')
    scan = ScansModel.query.filter_by(scan_id=scan_id).first()
    if not scan:
        msg = f'scan_id: {scan_id} not found'
        logger.info(msg)
        return action_response('failure', msg)
    return action_response('success', f'scan_id: {scan_id} status is: {scan.status}')


@app.route('/clean_up', methods=['GET'])
def clean_up_db() -> Dict[str, str]:
    delete_num = 0
    for scan in ScansModel.query:
        if scan.status == 'complete' and scan.finish_scanning_process_time + timedelta(minutes=20) < datetime.now():
            db.session.delete(scan)
            db.session.commit()
            logger.info(f'deleting scan_id: {scan.scan_id} from DB')
            delete_num += 1
    return action_response('success', f'deleted {delete_num} scans')


@app.errorhandler(404)
def default_handler(e):
    return Response(status=404)


if __name__ == '__main__':
    logger.debug('starting ingest server...')
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True)
