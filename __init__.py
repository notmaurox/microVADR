from flask_restplus import Api
from flask import Blueprint

from main.controller.vadr_controller import api as vadr_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API FOR VADR RUNS',
          version='1.0',
          description='flask VADR web service'
          )

api.add_namespace(vadr_ns, path='/vadr')