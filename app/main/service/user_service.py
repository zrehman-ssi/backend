import uuid
import datetime

from ..util.dto import ResponseDto,UserDto
from ..util.enums import ResponseStatus,UserType
from ..util.constants import Messages,GlobalSettings

from app.main import db
from app.main.model.user import User
from app.main.model.address import Address
from app.main.model.appointment_details import AppointmentDetails
from app.main.model.appointment import Appointment
from app.main.model.disease import Disease
from app.main.model.doctor_speciality import DoctorSpeciality
from app.main.model.doctor import Doctor
from app.main.model.file_info import FileInfo
from app.main.model.organization import Organization
from app.main.model.password_requests import PasswordRequests
from app.main.model.patient_disease import PatientDisease
from app.main.model.patient import Patient
from app.main.model.plan_disease import PlanDisease
from app.main.model.plan import Plan
from app.main.model.provider import Provider
from app.main.model.role import Role
from app.main.model.speciality import Speciality
from app.main.model.stakeholder import Stakeholder
from app.main.model.patient_plan import PatientPlan
from app.main.model.user_role import UserRole
 

 
_Messages = Messages
_user=UserDto.user
_Global_Settings = GlobalSettings

def saveNewUser(userDto):
    user = User.query.filter_by(email=userDto.email).first()
    if not user:
        user_with_username = User.query.filter_by(username=userDto.username).first()
        if(user_with_username is None):

            address_dto=Address(
                address1=userDto.address1,
                address2=userDto.address2,
                country=userDto.country,
                state=userDto.state,
                zip_code=userDto.zip_code,
                is_active=True,
                created_by=userDto.created_by,
                created_on=datetime.datetime.utcnow(),

            )
            address=saveChanges(address_dto) 

            new_user = User(
                
                first_name=userDto.first_name,
                last_name=userDto.last_name,
                username=userDto.username,
                email=userDto.email,
                password=userDto.password, 
                public_id=str(uuid.uuid4()),
                is_active=True,
                created_by=userDto.created_by,
                created_on=datetime.datetime.utcnow(), 
                user_type=userDto.user_type,  
                address_id=address.id,
                provider_id=userDto.provider_id,
                stakeholder_id=userDto.stakeholder_id,
                is_deleted=False

            )

            saved_user=saveChanges(new_user)

            if(userDto.user_type == UserType.PATIENT.value):
                patient= Patient(
                    user_id = saved_user.id,
                    provider_id = userDto.provider_id
                )
                saveChanges(patient)

            if(userDto.user_type == UserType.DOCTOR.value):
                doctor = Doctor(
                    duty_start_time = datetime.datetime.utcnow(),
                    duty_end_time = datetime.datetime.utcnow(),
                    user_id = saved_user.id,
                )
                saveChanges(doctor)
            
            response_object=ResponseDto()
            response_object.data=True,
            response_object.status = ResponseStatus.SUCCESS.value,
            response_object.message = _Messages.REGISTERED_SUCCESS
            response_object.status_code=201       
            return response_object
        else:
            response_object=ResponseDto()
            response_object.data=False,
            response_object.status = ResponseStatus.FAIL.value,
            response_object.message = _Messages.USERNAME_ALREADY_EXISTS 
            response_object.status_code=409       
            return response_object

    else:
        response_object=ResponseDto()
        response_object.data=False,
        response_object.status = ResponseStatus.FAIL.value,
        response_object.message = _Messages.EMAIL_ALREADY_EXISTS 
        response_object.status_code=409       
        return response_object  


def saveNewUsers(users):
    already_exists_usernames=[]
    already_exists_emails = []
    if(users is not None):
        for user in users:            
            response = saveNewUser(user)
            if(response.message==_Messages.USERNAME_ALREADY_EXISTS):
                already_exists_usernames.append(user.username)
            if(response.message==_Messages.EMAIL_ALREADY_EXISTS):
                already_exists_emails.append(user.email)

        return already_exists_usernames,already_exists_emails           


def getAllUsers():
    return User.query.all()


def getSingleUser(public_id):
    return User.query.filter_by(public_id=public_id).first()

def getUserByEmail(email):
    return User.query.filter_by(email=email).first()

def getUserByUsername(username):
    return User.query.filter_by(username=username).first()

def getUserById(id):
    return User.query.filter_by(id=id).first()

def isAdminUser(user_id):
    try:
      user =  User.query.filter_by(id=user_id).first()
      if(user is not None and user.user_type == UserType.ADMIN.value):
        return True
      else:
        return False  
    except Exception as e:
        print(e)
        return False
    return  False

def isPatient(patient_id):
    try:
      patient =  Patient.query.filter_by(id=patient_id).first()
      if(patient is not None):
          user = User.query.filter_by(id=patient.user_id).first()
          if(user is not None and user.user_type == UserType.PATIENT.value):
                return True   
          else:
                return False       

      else:
            return False  

    except Exception as e:
        print(e)
        return False
    return  False


def isDoctor(doctor_id):
    try:
      doctor =  Doctor.query.filter_by(id=doctor_id).first()
      if(doctor is not None):
          user = User.query.filter_by(id=doctor.user_id).first()
          if(user is not None and user.user_type == UserType.DOCTOR.value):
                return True   
          else:
                return False       

      else:
            return False  
            
    except Exception as e:
        print(e)
        return False
    return  False    

def saveChanges(data):
    db.session.add(data)
    db.session.commit()
    return data