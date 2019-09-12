import json,os

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.enums import OrganizationType

from ..util.dto import ResponseDto, DiseaseDto #Dto's

from ..util.dto import Disease #Api Model
 

from ..service.disease_service import saveDisease,getAllDiseases,getDiseaseById

api = DiseaseDto.api
_disease_dto = DiseaseDto.disease


@api.route('/allDiseases')
class Diseases(Resource):
    @api.doc('list_of_available_diseases')
    @api.marshal_list_with(_disease_dto, envelope='data')
    #@jwt_required
    def get(self):
        """List of all available diseases"""
        return getAllDiseases()


@api.route('/saveDisease')
class Disease(Resource):

    @api.doc('disease')
    @api.expect(_disease_dto, validate=True)
    #@jwt_required
    def post(self):
        """Save Disease"""        
         
        data = request.json
        if(data is not None):
            _diseaseDto = Disease()
            _diseaseDto.name = data['name']
            _diseaseDto.description = data['description']
            _diseaseDto.tags = data['tags']
            _diseaseDto.created_by = data['created_by']
            _diseaseDto.user_id = data['user_id'] # info : can be admin or provider

            saveDisease(_diseaseDto) 

            return ''
             
@api.route('/<disease_id>')
class DiseaseById(Resource):
    
    @api.doc('disease')
    @api.marshal_with(_disease_dto, envelope='data')
    #@jwt_required
    def get(self,disease_id):         
        return   getDiseaseById(disease_id)