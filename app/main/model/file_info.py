from .. import db

class FileInfo(db.Model):
    __tablename__ = "file_info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    guid = db.Column(db.String(48), nullable=True,unique=True)
    blob = db.Column(db.BLOB)
    fileName = db.Column(db.String(256), nullable=True,unique=False)

