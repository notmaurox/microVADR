import uuid
import datetime

from main import db
from main.model.main_model import VadrRun
from ..utils.utils import random_id

def start_new_run(data):
    vadr_run = VadrRun.query.filter_by(
        sequence=data['sequence'], sequence_name=data['sequence_name']
    ).first()
    if not vadr_run:
        new_vadr_run = VadrRun(
            process_id=9999,
            sequence_name=data['sequence_name'],
            sequence=data['sequence'],
            status='Submitted',
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_vadr_run)
        response_object = {
            'status': 'success',
            'message': 'New run submitted',
            'run_id': new_vadr_run.run_id,
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Something broke oopies',
            'run_id': None
        }
        return response_object, 409


def get_all_runs():
    return VadrRun.query.all()


def get_a_run(run_id):
    return VadrRun.query.filter_by(run_id=run_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()