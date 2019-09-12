from .. import db

class Speciality(db.Model):
    __tablename__ = "speciality"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    details = db.Column(db.String(512), nullable=True)
    reference = db.Column(db.String(128),nullable=False)
    created_by = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(128))
    modified_on = db.Column(db.DateTime)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

