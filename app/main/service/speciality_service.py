import uuid
import datetime

from ..util.enums import UserType,OrganizationType

from app.main import db # Database
 
from ..util.dto import SpecialityDto #Dto's

from app.main.model.speciality import Speciality #Database Model
from app.main.model.doctor import Doctor #Database Model
from app.main.model.doctor_speciality import DoctorSpeciality #Database Model

from ..service.user_service import isAdminUser,getUserById

def saveSpeciality(speciality):
    try:
        if(speciality is not None):
            if(isAdminUser(speciality.user_id)==True):

                specialityModel = Speciality(
                    name = speciality.name,
                    details = speciality.details,
                    reference = speciality.name,
                    created_by = speciality.created_by,
                    created_on = datetime.datetime.utcnow(),
                    is_deleted = False
                )
                data = saveChanges(specialityModel)
                return data

    except Exception as e:
        print(e)
        return None    
    return None

def getSpecialityById(speciality_id):
    return Speciality.query.filter_by(id=speciality_id).first()    

def getAllSpecialities():
    return Speciality.query.all()    

def getDoctorById(doctor_id):
    return Doctor.query.filter_by(id=doctor_id).first()

def saveDoctorSpecialities(doctorSpecialities):
    try:
        if(doctorSpecialities is not None and doctorSpecialities.specialities is not None):
            if(isAdminUser(doctorSpecialities.user_id)==True):
                doctor = getDoctorById(doctorSpecialities.doctor_id)                
                if(doctor is not None ):
                    user = getUserById(doctor.user_id)
                    if(user is not None and user.user_type == UserType.DOCTOR.value):
                        for specialityId in doctorSpecialities.specialities:
                            speciality = getSpecialityById(specialityId)
                            if(speciality is not None):

                                doctorSpecialityModel = DoctorSpeciality(
                                    doctor_id=doctorSpecialities.doctor_id,
                                    speciality_id=specialityId)

                                saveChanges(doctorSpecialityModel) 

                        return  ''

    except Exception as e:
        print(e)
        return None    
    return None

def saveChanges(data):
    db.session.add(data)
    db.session.commit()
    return data    