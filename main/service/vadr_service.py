import uuid
import datetime
import random
import os

from main import db
from main.model.main_model import VadrRun
from ..utils.vadr_runner import VadrRunner

def validate_password(data):
    vadr_pass = os.getenv("MICROVADRPASS")
    if vadr_pass:
        return vadr_pass == data['password']
    else:
        return "iamyourfather" == data['password']

def start_new_run(data):
    if not validate_password(data):
        response_object = {
            'status': 'fail',
            'message': 'bad password',
            'process_id': None
        }
        return response_object, 409
    vadr_run = VadrRun.query.filter_by(
        sequence=data['sequence'], sequence_name=data['sequence_name']
    ).first()
    # if someone is submitting the same sequence as previously seen before
    # return the results we already have maybe? space considerations?
    try:
        process_id = random.randint(10000000, 99999999)
        while VadrRunner.is_run_dir(process_id):
            process_id = random.randint(10000000, 99999999)
        new_vadr_run = VadrRun(
            process_id=process_id,
            sequence_name=data['sequence_name'],
            sequence=data['sequence'],
            status='Submitted',
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_vadr_run)
        response_object = {
            'status': 'success',
            'message': 'New run submitted',
            'process_id': new_vadr_run.process_id,
        }
        VadrRunner(
            seq_name=data['sequence_name'],
            seq=data['sequence'],
            process_id=process_id,
        ).go()
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e),
            'process_id': None
        }
        return response_object, 500


def get_all_runs():
    return VadrRun.query.all()


def get_a_run(process_id):
    return VadrRun.query.filter_by(process_id=process_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()