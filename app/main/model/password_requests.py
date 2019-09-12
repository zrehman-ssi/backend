from .. import db

class PasswordRequests(db.Model):
    __tablename__ = "password_requests"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(128), nullable=True,unique=True)
    created_on = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

