from .. import db

class PatientDisease(db.Model):
    __tablename__ = "patient_disease"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'))

