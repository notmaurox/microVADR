from flask_restplus import Namespace, fields

class VadrRunDto:
    api = Namespace('vadrrun', description='vadrrun related operations')
    vadr_run = api.model('vadrrun', {
        'sequence_name': fields.String(required=True, description='user email address'),
        'sequence': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='password to submit run (default: iamyourfather, can overwrite with MICROVADRPASS env variable within docker-compose file)'),
    })