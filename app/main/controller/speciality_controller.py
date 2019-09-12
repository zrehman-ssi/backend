import json,os

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.enums import OrganizationType

from ..util.dto import ResponseDto, SpecialityDto #Dto's

from ..util.dto import SpecialityDto,Speciality,DoctorSpecialities #Api Model
 

from ..service.speciality_service import getAllSpecialities,saveSpeciality,getSpecialityById,saveDoctorSpecialities

api = SpecialityDto.api
_speciality_dto = SpecialityDto.speciality
_doctor_speciality_dto = SpecialityDto.doctor_speciality

@api.route('/allSpecialities')
class Specialities(Resource):
    @api.doc('list_of_available_specialities')
    @api.marshal_list_with(_speciality_dto, envelope='data')
    #@jwt_required
    def get(self):
        """List of all available specialities"""
        return getAllSpecialities()


@api.route('/saveSpeciality')
class Speciality(Resource):

    @api.doc('speciality')
    @api.expect(_speciality_dto, validate=True)
    #@jwt_required
    def post(self):
        """Save Speciality"""        
         
        data = request.json
        if(data is not None):
             
            _specialityDto = Speciality()
            _specialityDto.name = data['name']
            _specialityDto.details = data['details']
            _specialityDto.reference = data['reference']
            _specialityDto.created_by = data['created_by']           
            _specialityDto.user_id=data['user_id']

            saveSpeciality(_specialityDto)

            return ''


@api.route('/saveDoctorSpecialities')
class DoctorSpecialities(Resource):

    @api.doc('doctor specialities')
    @api.expect(_doctor_speciality_dto, validate=True)
    #@jwt_required
    def post(self):
        """Save Doctor Specialities"""        
         
        data = request.json
        if(data is not None):
             
            _doctorSpecialitiesDto = DoctorSpecialities()
            _doctorSpecialitiesDto.doctor_id = data['doctor_id']
            _doctorSpecialitiesDto.user_id = data['user_id']
            _doctorSpecialitiesDto.specialities = data['specialities']
             

            saveDoctorSpecialities(_doctorSpecialitiesDto)

            return ''

             
@api.route('/<speciality_id>')
class SpecialityById(Resource):
    
    @api.doc('speciality by id')
    @api.marshal_with(_speciality_dto, envelope='data')
    #@jwt_required
    def get(self,speciality_id):         
        return   getSpecialityById(speciality_id)