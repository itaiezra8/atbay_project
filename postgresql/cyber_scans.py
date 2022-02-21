from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ScansModel(db.Model):
    __tablename__ = 'cyber_scans'

    scan_id = db.Column(db.String(), primary_key=True)
    scan_req_time = db.Column(db.TIME())
    start_scanning_process_time = db.Column(db.TIME())
    finish_scanning_process_time = db.Column(db.TIME())
    status = db.Column(db.String())

    def __init__(self, scan_id, scan_req_time, status):
        self.scan_id = scan_id
        self.scan_req_time = scan_req_time
        # self.start_scanning_process_time = start_scanning_process_time
        # self.finish_scanning_process_time = finish_scanning_process_time
        self.status = status

    def __repr__(self):
        return f'scan {self.scan_id}'