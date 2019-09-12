import uuid
import datetime

from ..util.enums import UserType,OrganizationType

from app.main import db # Database
 
from ..util.dto import AppointmentDto #Dto's

from app.main.model.appointment import Appointment #Database Model

from ..service.user_service import isAdminUser

def getAllAppointments():
    return Appointment.query.all()    


def saveChanges(data):
    db.session.add(data)
    db.session.commit()
    return data  