from .. import db

class PlanDisease(db.Model):
    __tablename__ = "plan_disease"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
    disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'))

