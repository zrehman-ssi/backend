from .. import db

class PatientPlan(db.Model):
    __tablename__ = "patient_plan"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))

