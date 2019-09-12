from .. import db
from sqlalchemy.orm import relationship

class Provider(db.Model):
    __tablename__ = "provider"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id')) 
    organization = relationship("Organization")
