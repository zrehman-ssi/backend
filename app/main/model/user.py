from .. import db, flask_bcrypt 
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128))
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    public_id = db.Column(db.String(128), unique=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_by = db.Column(db.String(128))
    created_on = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(128))
    modified_on = db.Column(db.DateTime)
    user_type = db.Column(db.Integer)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id') , nullable=True)
    stakeholder_id = db.Column(db.Integer, db.ForeignKey('stakeholder.id'), nullable=True)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    address = relationship("Address")

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)
