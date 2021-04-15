from flask import request
from flask_restplus import Resource

from ..dtos.dto import VadrRunDto
from ..service.vadr_service import start_new_run, get_all_runs, get_a_run
from ..utils.vadr_runner import VadrRunner, VadrResultsFtr

api = VadrRunDto.api
_vadrrun = VadrRunDto.vadr_run


@api.route('/')
class VadrRunList(Resource):
    @api.doc('list_of_vadr_runs')
    @api.marshal_list_with(_vadrrun, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_runs()

    @api.response(201, 'Run successfully created.')
    @api.doc('create a new VADR run')
    @api.expect(_vadrrun, validate=True)
    def post(self):
        """creates new VADR run"""
        data = request.json
        return start_new_run(data=data)


@api.route('/<process_id>')
@api.param('process_id', 'Process ID returned from posting sequence')
@api.response(404, 'Run not found.')
class VadrRun(Resource):
    @api.doc('get a Run')
    # @api.marshal_with(_vadrrun)
    def get(self, process_id):
        """get a user given its identifier"""
        vadr_run = get_a_run(process_id)
        runner = VadrRunner(
            seq_name=vadr_run.sequence_name,
            seq=vadr_run.sequence,
            process_id=vadr_run.process_id,
        )
        runner.go()
        to_return ={
            'sequence_name': vadr_run.sequence_name,
            'sequence': vadr_run.sequence,
            'results': runner.get_results()
        }
        return to_return
