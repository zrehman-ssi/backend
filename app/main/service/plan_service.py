import uuid
import datetime

from ..util.enums import UserType,OrganizationType

from app.main import db # Database

from ..util.dto import PlanDto #Dto's

from app.main.model.user import User #Database Model
from app.main.model.organization import Organization #Database Model
from app.main.model.provider import Provider #Database Model
from app.main.model.stakeholder import Stakeholder #Database Model
from app.main.model.address import Address #Database Model
from app.main.model.plan import Plan #Database Model
from app.main.model.plan_disease import PlanDisease #Database Model
from app.main.model.patient_plan import PatientPlan #Database Model
from app.main.model.patient_disease import PatientDisease #Database Model
from app.main.model.patient import Patient #Database Model

from ..service.disease_service import getDiseaseById
from ..service.user_service import getUserById,isPatient
from ..service.organization_service import isProvider,isStakeholder

def providerPlanSignup(providerPlan):

    try:
        if(providerPlan is not None):

            if(isProvider(providerPlan.provider_id)==True):
                providerPlanModel = Plan(
                    provider_id = providerPlan.provider_id,
                    created_by = providerPlan.created_by,
                    created_on = datetime.datetime.utcnow()
                )
                data = saveChanges(providerPlanModel)
                if(data is not None ):
                    providerPlan.id=data.id
                    saveProviderPlanDiseases(providerPlan)
                    return data

    except Exception as e:
        print(e)
        return None    
    return None


def saveProviderPlanDiseases(providerPlan):
    if(providerPlan is not None and providerPlan.diseases is not None):
        for diseaseId in providerPlan.diseases:
            disease = getDiseaseById(diseaseId)
            if(disease is not None):
                plan_disease_rel= PlanDisease(
                    plan_id = providerPlan.id,
                    disease_id = disease.id
                )
                saveChanges(plan_disease_rel)


def patientPlanSignup(patientPlan):
    try:
         plan = getPlanById(patientPlan.plan_id)
         if(plan is not None):
            
            patientPlanModel = PatientPlan(
                patient_id = patientPlan.patient_id,
                plan_id = patientPlan.plan_id
            )
            data = saveChanges(patientPlanModel)
            if(data is not None ):
                savePatientPlanDiseases(patientPlan)
                return data

    except Exception as e:
            print(e)
            return None    
      


def savePatientPlanDiseases(patientPlan):
    if(patientPlan is not None and patientPlan.diseases is not None):
        isUserPatient = isPatient(patientPlan.patient_id)==True
        for diseaseId in patientPlan.diseases:
            disease = getDiseaseById(diseaseId)
            if(disease is not None and isUserPatient==True):
                patient_disease_rel= PatientDisease(
                            patient_id = patientPlan.patient_id,
                            disease_id = diseaseId
                        )
                saveChanges(patient_disease_rel)
                
                        


def getPlanById(plan_id):
    return Plan.query.filter_by(id=plan_id).first()

def getPlansByPatientId(patient_id):
    return PatientPlan.query.filter_by(patient_id=patient_id)   

def getAllPatientPlans():
    return PatientPlan.query.all()

def getAllProviderPlans():
    return Plan.query.all()    

def getPatientById(patient_id):
    return Patient.query.filter_by(id=patient_id).first()

def saveChanges(data):
    db.session.add(data)
    db.session.commit()
    return data      