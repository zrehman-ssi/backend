from .. import db

class AppointmentDetails(db.Model):
    __tablename__ = "appointment_details"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_date = db.Column(db.DateTime, nullable=False)     
    created_by = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(128))
    modified_on = db.Column(db.DateTime)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
