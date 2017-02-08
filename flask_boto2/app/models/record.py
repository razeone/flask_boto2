from app import db
import datetime


class PathTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    path = db.Column(db.String(120))
    last_refresh = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, _id, name, path):
        self.id = _id
        self.name = name
        self.path = path
        self.last_refresh = datetime.datetime.now()
