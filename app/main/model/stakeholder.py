from .. import db
from sqlalchemy.orm import relationship

class Stakeholder(db.Model):
    __tablename__ = "stakeholder"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id')) 
    budget = db.Column(db.Integer, nullable=False)
    organization = relationship("Organization")

