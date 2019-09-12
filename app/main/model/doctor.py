from .. import db

class Doctor(db.Model):
    __tablename__ = "doctor"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    duty_start_time = db.Column(db.DateTime, nullable=False)
    duty_end_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

