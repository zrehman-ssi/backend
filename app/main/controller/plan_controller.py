import json,os

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.enums import OrganizationType

from ..util.dto import ResponseDto, PlanDto #Dto's

from ..util.dto import ProviderPlan #Api Model
from ..util.dto import PatientPlan #Api Model

from ..service.plan_service import providerPlanSignup,patientPlanSignup,getAllPatientPlans,getAllProviderPlans

api = PlanDto.api
_providerPlan_dto = PlanDto.providerPlan
_patientPlan_dto=PlanDto.patientPlan 

@api.route('/allProviderPlans')
class ProviderPlanList(Resource):
    @api.doc('list_of_available_provider_plans')
    @api.marshal_list_with(_providerPlan_dto, envelope='data')
    #@jwt_required
    def get(self):
        """List of all available provider plans"""
        return getAllProviderPlans()


@api.route('/allPatientPlans')
class PatientPlanList(Resource):
    @api.doc('list_of_available__patient_plans')
    @api.marshal_list_with(_patientPlan_dto, envelope='data')
    #@jwt_required
    def get(self):
        """List of all available patient plans"""
        return getAllPatientPlans()


@api.route('/providerPlanSignup')
class ProviderPlanSignup(Resource):

    @api.doc('provider plan signup')
    @api.expect(_providerPlan_dto, validate=True)
    #@jwt_required
    def post(self):
        """Signup Provider Plan"""        
         
        data = request.json
        if(data is not None):
            providerPlanDto=ProviderPlan()
            providerPlanDto.provider_id=data['provider_id']
            providerPlanDto.created_by=data['created_by']
            providerPlanDto.diseases=data['diseases']

            providerPlanSignup(providerPlanDto)
            return ''
             

@api.route('/patientPlanSignup')
class PatientPlanSignup(Resource):

    @api.doc('patient plan signup')
    @api.expect(_patientPlan_dto, validate=True)
    #@jwt_required
    def post(self):
        """Signup Patient Plan"""        
         
        data = request.json
        if(data is not None):
            patientPlanDto= PatientPlan()
            patientPlanDto.patient_id=data['patient_id']
            patientPlanDto.plan_id=data['plan_id']
            patientPlanDto.diseases=data['diseases']
            patientPlanSignup(patientPlanDto)
            return ''