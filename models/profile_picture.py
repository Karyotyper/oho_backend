from . import db
from marshmallow import fields, Schema


class profile_picture(db.Model):
    __tablename__ = 'prompt'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_simpleton.id'))
    caption = db.Column(db.String(500), nullable = True)

    def __init__(self, data):
        self.path = data.get("path")
        self.user_id = data.get("user_id")
        self.caption = data.get("caption")
