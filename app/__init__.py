# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.file_controller import api as file_ns
from .main.controller.organization_controller import api as organization_ns
from .main.controller.plan_controller import api as plan_ns
from .main.controller.disease_controller import api as disease_ns
from .main.controller.speciality_controller import api as speciality_ns
from .main.controller.appointment_controller import api as appointment_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint, 
          title='SIB API',
          version='1.0',
          description='An API for Resillient Wellness application.',
          ui=False
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(file_ns, path='/file')
api.add_namespace(organization_ns, path='/organization')
api.add_namespace(plan_ns, path='/plan')
api.add_namespace(disease_ns, path='/disease')
api.add_namespace(speciality_ns, path='/speciality')
api.add_namespace(appointment_ns, path='/appointment')