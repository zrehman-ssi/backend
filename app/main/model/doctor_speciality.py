from .. import db

class DoctorSpeciality(db.Model):
    __tablename__ = "doctor_speciality"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    speciality_id = db.Column(db.Integer, db.ForeignKey('speciality.id'))

