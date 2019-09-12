from .. import db 
from sqlalchemy.orm import relationship

class Organization(db.Model):
    __tablename__ = "organization"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    phone_number = db.Column(db.String(32),nullable=False)
    email = db.Column(db.String(128),nullable=False)
    organization_type = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_by = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(128))
    modified_on = db.Column(db.DateTime)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    stakeholder = relationship("Stakeholder")
    provider = relationship("Provider")
    address = relationship("Address")