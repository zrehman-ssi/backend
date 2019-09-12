from .. import db

class Plan(db.Model):
    __tablename__ = "plan"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    created_by = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(128))
    modified_on = db.Column(db.DateTime)

