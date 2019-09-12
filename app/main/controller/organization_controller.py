import json,os

from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..util.enums import OrganizationType

from ..util.dto import ResponseDto, OrganizationDto,JsonSerializable #Dto's
from ..util.dto import Organization,Stakeholder,Provider ,Address,StakeholderFilter#Api Models
from ..service.organization_service import getAllOrganizations,getOrganizationById,registerOrganization,getAllProviders,getProviderById,getAllStakeholders,getStakeholderById,registerProvider,registerStakeholder,getStakeholderDetails

api = OrganizationDto.api
_organization_dto = OrganizationDto.organization 
_stakeholder_dto = OrganizationDto.stakeholder
_provider_dto = OrganizationDto.provider
_stakeholder_details_dto = OrganizationDto.stakeholder_details
 


@api.route('/')
class OrganizationList(Resource):
    @api.doc('list_of_available_organizations')
    @api.marshal_list_with(_organization_dto, envelope='data')
    #@jwt_required
    def get(self):
        """List all available organizations"""
        return getAllOrganizations()


@api.route('/provider')
class Provider(Resource):
    @api.doc('provider register')
    @api.expect(_provider_dto, validate=True)
    #@jwt_required
    def post(self):
        """Register Provider"""        
         
        data = request.json
        if(data is not None):
            _organizationDto=Organization()
            _organizationDto.name = data['name']
            _organizationDto.email = data['email']
            _organizationDto.phone_number = data['phone_number']
            _organizationDto.user_id = data['user_id']
            _organizationDto.organization_type = OrganizationType.PROVIDER.value

            # Address Dto
            _organizationDto.address=Address()
            _organizationDto.address.address1= data['address1']
            _organizationDto.address.address2= data['address2']
            _organizationDto.address.country= data['country']
            _organizationDto.address.zip_code= data['zip_code']
            _organizationDto.address.state= data['state']

            # Provider Dto
            _organizationDto.provider=Provider()
            

            organization = registerOrganization(_organizationDto) 
            if(organization is not None):

                return  

@api.route('/<provider_id>')
class ProviderById(Resource):
    
    @api.doc('provider')
    @api.marshal_with(_provider_dto, envelope='data')
    #@jwt_required
    def get(self,provider_id):         
        return    getProviderById(provider_id) 
        
@api.route('/allProviders')
class Providers(Resource):

    @api.doc('all providers')
    @api.marshal_list_with(_provider_dto, envelope='data')
    #@jwt_required
    def get(self):
        return getAllProviders()


@api.route('/stakeholder')
class Stakeholder(Resource):

    @api.doc('stakeholder register')
    @api.expect(_stakeholder_dto, validate=True)
    #@jwt_required
    def post(self):
        """Register Stakeholder""" 
        data = request.json
        if(data is not None):
            _organizationDto=Organization()
            _organizationDto.name = data['name']
            _organizationDto.email = data['email']
            _organizationDto.phone_number = data['phone_number']
            _organizationDto.user_id = data['user_id']
            _organizationDto.organization_type = OrganizationType.STAKEHOLDER.value

            # Address Dto
            _organizationDto.address=Address()
            _organizationDto.address.address1= data['address1']
            _organizationDto.address.address2= data['address2']
            _organizationDto.address.country= data['country']
            _organizationDto.address.zip_code= data['zip_code']
            _organizationDto.address.state= data['state']

            # Stakeholder Dto
            _organizationDto.stakeholder=Stakeholder()
            _organizationDto.stakeholder.budget=data['budget']

            organization = registerOrganization(_organizationDto) 
            if(organization is not None):

                return


@api.route('/<stakeholder_id>')
class StakeholderById(Resource):
   
    @api.doc('stakeholder')
    @api.marshal_with(_stakeholder_dto, envelope='data')
    #@jwt_required
    def get(self,stakeholder_id):
        return getStakeholderById(stakeholder_id)       


@api.route('/allStakeholders')
class Stakeholders(Resource):

    @api.doc('all stakeholders')
    @api.marshal_list_with(_stakeholder_dto, envelope='data')
    #@jwt_required
    def get(self):         
        return  getAllStakeholders()       

@api.route('/getStakeholdersDetails/id=<stakeholder_id>/filter=<filters>')
class  StakeholdersFilter(Resource):
    @api.doc('stakeholder details')     
    @api.marshal_list_with(_stakeholder_details_dto, envelope='data')
    #@jwt_required
    def get(self,stakeholder_id,filters):
         
        stakeholderFilter=StakeholderFilter()
        stakeholderFilter.id = int(stakeholder_id)

        receivedFilters = filters.split('&&')
        filtersDic = dict()

        for filter in receivedFilters:
            filtersDic.update({filter.split('=')[0].replace(" ", "").lower() : int(filter.split('=')[1].lower())})

        stakeholderFilter.provider= filtersDic.get('provider')
        stakeholderFilter.department= filtersDic.get('department')
        stakeholderFilter.doctor= filtersDic.get('doctor')

        stakeholders = getStakeholderDetails(stakeholderFilter)
         

        return    stakeholders   
            