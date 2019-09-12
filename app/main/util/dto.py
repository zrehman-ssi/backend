import json,datetime
from flask_restplus import Namespace, fields
from ..util.enums import UserType

"""Api models"""
class JsonSerializable(object):
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)

    def __repr__(self):
        return self.toJson()

class ResponseDto(JsonSerializable):

    status = None
    status_code=None
    message = None
    data = None

class FileInfo():
    rows = []
       

class User():
    first_name=''     
    last_name='' 
    email=''
    username=''
    password=''
    user_type=0
    address1=''
    address2=''
    country=''
    state='' 
    zip_code=''
    provider_id=0
    stakeholder_id=0


class Organization():
    id=0
    name=''     
    organization_type=0    
    phone_number =''
    email= ''
    user_id=0
    created_by=''
    created_on=datetime.datetime.utcnow()
    address=object
    stakeholder=object
    provider=object

class Provider(Organization):
    id=0     
    organization_id=0


class Stakeholder(Organization):
    id=0
    organization_id=0
    budget=0    

class Address():
    id=0
    address1 = ''
    address2 = ''
    country = ''
    state = ''
    zip_code = ''
    is_active = True
    created_by = ''
     
class ProviderPlan():
    id = 0
    provider_id = 0
    created_by = ''    
    diseases=list

class PatientPlan():
    id=0
    patient_id = 0
    plan_id = 0
    diseases=list

class Disease(): 
    id=0 
    name=''         
    description='' 
    tags=''
    created_by =''
    user_id=0

class Speciality():
    id=0 
    name=''         
    details='' 
    reference=''
    created_by =''
    user_id=0

class DoctorSpecialities():
    id = 0
    doctor_id = 0
    specialities=list
    user_id=0


class Appointment():
    id = 0
    name = ''    

class StakeholderFilter():
    id = 0
    provider = 0 
    department = 0
    doctor = 0    

"""Api Dto's"""

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'first_name': fields.String(required=True, description='user first name'),
        'last_name': fields.String(required=True, description='user last name'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier'),
        'user_type': fields.Integer(required=True,description='user type'),
        'address1' : fields.String(description='Address 1'),
        'address2' : fields.String(description='Address 2'),
        'country' : fields.String(description='Country Name'),
        'state' : fields.String(description='State Name'),
        'zip_code' : fields.String(description='Zip Code'),
        'provider_id' : fields.Integer(description='Provider Id'),
        'stakeholder_id' : fields.Integer(description='Stakeholder Id')
    })

class AuthDto():
    api= Namespace('auth',description='authentication related operations')

    """ login dto"""
    login=api.model('login',{
        'username': fields.String(required=True, description='user username'),         
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
    })

    """ password request dto"""
    password_request = api.model('password_request',{
        'username': fields.String(required=True, description='user username'),         
        'email': fields.String(required=True, description='user email address')         
    }  )

    """ reset password dto """
    reset_password = api.model('reset_password',{
        'token': fields.String(required=True, description='token'),
        'new_password': fields.String(required=True, description='New Password'),
    })

class FileInfoDto():
    api= Namespace('file',description='files related operations')

    """file info dto"""
    file_info=api.model('file_info',{
        'user_id': fields.Integer(required=True, description='user id'),
        'guid': fields.String(required=False, description='file guid')
    })


class OrganizationDto():
    api= Namespace('organization',description='organization related operations')

    """organization info dto"""
    organization = api.model('organization',{
        'id': fields.Integer(required=False, description='id'),
        'name': fields.String(required=True, description='organization name'),         
        'organization_type': fields.Integer(required=True,description='user type'),
        'address1' : fields.String(description='Address 1'),
        'address2' : fields.String(description='Address 2'),
        'country' : fields.String(description='Country Name'),
        'state' : fields.String(description='State Name'),
        'zip_code' : fields.String(description='Zip Code'),
        'phone_number' : fields.String(description='phone number'),
        'email' : fields.String(description='organization email')
    })    

    """provider info dto"""
    provider = api.model('provider',{
        'id': fields.Integer(required=False, description='id'),
        'name': fields.String(required=True, description='organization name'),
        'address1' : fields.String(description='Address 1'),
        'address2' : fields.String(description='Address 2'),
        'country' : fields.String(description='Country Name'),
        'state' : fields.String(description='State Name'),
        'zip_code' : fields.String(description='Zip Code'),
        'phone_number' : fields.String(description='phone number'),
        'email' : fields.String(description='organization email'),
        'user_id': fields.Integer(required=True, description='user id'),
        'organization_id': fields.Integer(required=False, description='organization id'),
    })    

    """stakeholder info dto"""
    stakeholder = api.model('stakeholder',{
        'id': fields.Integer(required=False, description='id'),
        'name': fields.String(required=True, description='organization name'),    
        'address1' : fields.String(description='Address 1'),
        'address2' : fields.String(description='Address 2'),
        'country' : fields.String(description='Country Name'),
        'state' : fields.String(description='State Name'),
        'zip_code' : fields.String(description='Zip Code'),
        'phone_number' : fields.String(description='phone number'),
        'email' : fields.String(description='organization email'),         
        'budget': fields.Integer(required=True, description='budget'),
        'user_id': fields.Integer(required=True, description='user id'),
        'organization_id': fields.Integer(required=False, description='organization id'),
    })    

    """stakeholder details info dto"""
    stakeholder_details =  api.model('stakeholder_details',{
        'id': fields.Integer(required=False, description='id'),
        'name': fields.String(required=False, description='organization name'), 
        'users':fields.List(fields.Nested(UserDto.user))
    })  
     

class PlanDto():
    api= Namespace('plan',description='plan related operations')

    """Provider Plan Dto"""
    providerPlan = api.model('providerPlan',{
        'id': fields.Integer(required=False, description='id'),
        'provider_id': fields.Integer(required=True, description='user id'),
        'created_by' : fields.String(description='created by'),
        'diseases' : fields.List(fields.Integer, description='diseases', required=True)
        })   
     
    """Patient Plan Dto"""
    patientPlan = api.model('patientPlan',{
         'id': fields.Integer(required=False, description='id'),
         'patient_id': fields.Integer(required=True, description='patient id'),
         'plan_id': fields.Integer(required=True, description='plan id'),
         'diseases' : fields.List(fields.Integer, description='diseases', required=True)
        })    


class DiseaseDto():
    api= Namespace('disease',description='disease related operations')

    """Disease Dto"""
    disease = api.model('disease',{
        'id': fields.Integer(required=False, description='id'),
        'name': fields.String(required=True, description='disease name'),         
        'description': fields.String(description='disease description'),
        'tags' : fields.String(description='search index tags'),
        'created_by' : fields.String(description='created by'),
        'user_id': fields.Integer(required=True, description='user id'),
        })   
     


class SpecialityDto():
    api= Namespace('speciality',description='specialities related operations')

    """Speciality Dto"""
    speciality = api.model('speciality',{
        'id': fields.Integer(required=False, description='id'),
        'name': fields.String(required=True, description='speciality name'),         
        'details': fields.String(description='speciality details'),
        'reference' : fields.String(description='references'),
        'created_by' : fields.String(description='created by'),
        'user_id': fields.Integer(required=True, description='user id')
        })   
     

    """Patient Plan Dto"""
    doctor_speciality = api.model('doctor_speciality',{          
         'doctor_id': fields.Integer(required=True, description='doctor id'),
         'specialities' : fields.List(fields.Integer, description='specialities', required=True),
         'user_id': fields.Integer(required=True, description='user id') 
        })    


class AppointmentDto():
    api= Namespace('appointment',description='appointment related operations')

    """Appointment Dto"""
    appointment = api.model('appointment',{
        'id': fields.Integer(required=False, description='id'),
        'name': fields.String(required=True, description='speciality name')
        })   
     