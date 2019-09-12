from .. import db

class Address(db.Model):
    __tablename__ = "address"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address1 = db.Column(db.String(256), nullable=False)
    address2 = db.Column(db.String(256), nullable=True)
    country = db.Column(db.String(64),nullable=False)
    state = db.Column(db.String(128),nullable=False)
    zip_code = db.Column(db.String(16),nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_by = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(128))
    modified_on = db.Column(db.DateTime)

