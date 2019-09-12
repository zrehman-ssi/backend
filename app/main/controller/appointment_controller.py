import json,os

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.enums import OrganizationType

from ..util.dto import ResponseDto,AppointmentDto #Dto's

from ..util.dto import Appointment #Api Model
 
from ..service.appointment_service import getAllAppointments



api = AppointmentDto.api
_appointment_dto = AppointmentDto.appointment


@api.route('/allAppointments')
class Appointments(Resource):
    @api.doc('list_of_available_appointments')
    @api.marshal_list_with(_appointment_dto, envelope='data')
    #@jwt_required
    def get(self):
        """List of all available appointments"""
        return getAllAppointments()
