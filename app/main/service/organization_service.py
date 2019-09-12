import uuid
import datetime

from ..util.enums import UserType,OrganizationType

from app.main import db # Database

from ..util.dto import OrganizationDto #Dto's

from app.main.model.user import User
from app.main.model.organization import Organization #Database Model
from app.main.model.provider import Provider #Database Model
from app.main.model.stakeholder import Stakeholder #Database Model
from app.main.model.address import Address #Database Model



def saveAddress(address):
    try:
        if(address is not None):

            addressModel = Address(
                address1 = address.address1,
                address2 = address.address2,
                country = address.country,
                state = address.state,
                zip_code = address.zip_code,
                is_active = True,
                created_by = address.created_by,
                created_on = datetime.datetime.utcnow()
            )
            data = saveChanges(addressModel)
            return data

    except Exception as e:
        print(e)
        return None    
    return None
    

def getAllOrganizations():
    return Organization.query.all()

def registerOrganization(organization):
    try:
        if(organization is not None):
            user = User.query.filter_by(id=organization.user_id).first()
            if(user is not None and user.user_type == UserType.ADMIN.value):
                
                organization.user_id=user.id

                address = saveAddress(organization.address)
                if(address is None):
                    return None


                organizationModel = Organization(
                    name =  organization.name,
                    address_id =  address.id,
                    phone_number =  organization.phone_number,
                    email =  organization.email,
                    organization_type =  organization.organization_type,
                    is_active =  True,
                    created_by =  user.username,
                    created_on =  datetime.datetime.utcnow(),
                    is_deleted = False                    
                )
                data = saveChanges(organizationModel)

                if(data is not None):
                    organization.id= data.id
                    if(data.organization_type==OrganizationType.STAKEHOLDER.value):
                        organization.stakeholder.organization_id=data.id
                        registerStakeholder(organization.stakeholder)
                    if(data.organization_type==OrganizationType.PROVIDER.value):
                        organization.provider.organization_id=data.id
                        registerProvider(organization.provider)    
                return data

    except Exception as e:
        print(e)
        return None    
    return None

def getOrganizationById(organization_id):
    return Organization.query.filter_by(id=organization_id).first()



def getAllProviders():
    return Provider.query.all()   

def registerProvider(provider):
    try:
        if(provider is not None):
            providerModel = Provider(
                    organization_id=provider.organization_id                     
                )

            data = saveChanges(providerModel)
            return data

        else:
            return None    

    except Exception as e:
        print(e)
        return None    
    return None    

def getProviderById(provider_id):
    return Provider.query.filter_by(id=provider_id).first()



def getAllStakeholders():
    return Stakeholder.query.all()

def registerStakeholder(stakeholder):
    try:
        if(stakeholder is not None):
            stakeholderModel = Stakeholder(
                organization_id=stakeholder.organization_id,
                budget=stakeholder.budget
            )

            data = saveChanges(stakeholderModel)
            return data

        else:
            return None        
                

    except Exception as e:
        print(e)
        return None    
    return None   

def getStakeholderById(stakeholder_id):
    return Stakeholder.query.filter_by(id=stakeholder_id)


def isProvider(provider_id):
    provider = getProviderById(provider_id)
    if(provider is not None):
        organization = getOrganizationById(provider.organization_id)
        if(organization is not None and organization.organization_type == OrganizationType.PROVIDER.value):
            return True
        else:
            return False

    else:
        return False

def isStakeholder(stakeholder_id):
    stakeholder = getStakeholderById(stakeholder_id)
    if(stakeholder is not None):
        organization = getOrganizationById(stakeholder.organization_id)
        if(organization is not None and organization.organization_type == OrganizationType.STAKEHOLDER.value):
            return True
        else:
            return False
            
    else:
        return False

def getStakeholderDetails(stakeholderFilter):
    if(stakeholderFilter is not None):
        if(stakeholderFilter.id==0):
            stakeholders = Stakeholder.query.all()
            if(stakeholders is not None):
                for stakeholder in stakeholders:
                    stakeholder.name = stakeholder.organization.name
                    stakeholder.users = getPatientsByStakeholderId(stakeholder.id)

            return stakeholders
        else:
            stakeholder = Stakeholder.query.filter_by(id=stakeholderFilter.id).first()
            if(stakeholder is not None):

                stakeholder.name = stakeholder.organization.name
                stakeholder.users = getPatientsByStakeholderId(stakeholderFilter.id)

                return [stakeholder]


def getPatientsByStakeholderId(stakeholderId):

    users = User.query.filter_by(stakeholder_id=stakeholderId).all()
    if(users is not None):
        for user in users:
             
            if(user.address is not None):
                user.address1=user.address.address1
                user.address2=user.address.address2
                user.country =user.address.country
                user.state = user.address.state
                user.zip_code = user.address.zip_code
    return users

def saveChanges(data):
    db.session.add(data)
    db.session.commit()
    return data