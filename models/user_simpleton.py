from marshmallow import fields, Schema
import datetime

from sqlalchemy import ForeignKey, Date

from . import db
from sqlalchemy.orm import relationships


class user_simpleton(db.Model):
    __tablename__ = 'user_simpleton'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(2), nullable=True)
    occupation = db.Column(db.String(50), nullable=True)
    preferred_gender = db.Column(db.String(2), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    dob = db.Column(db.String(50), nullable=True)

    bio = db.Column(db.String(500), nullable=True)
    height_inch_min = db.Column(db.Integer, nullable=True)
    height_inch_max = db.Column(db.Integer, nullable=True)
    height_ft_min = db.Column(db.Integer, nullable=True)
    height_ft_max = db.Column(db.Integer, nullable=True)
    education = db.Column(db.String(50), nullable=True)

    preferred_race = db.Column(db.String(50), nullable=True)
    preferred_religion = db.Column(db.String(50), nullable=True)
    budget_range = db.Column(db.String(50), nullable=True)
    preferred_education = db.Column(db.String(50), nullable=True)
    active_hour = db.Column(db.String(50), nullable=True)
    preferred_location = db.Column(db.String(50), nullable=True)
    proximity_range = db.Column(db.String(50), nullable=True)

    prompts = db.relationship('prompt', backref='user_simpleton',
                              lazy='dynamic')

    def __init__(self, data):
        self.name = data.get('name')
        self.email = data.get('email')
        self.phone = data.get('phone')
        self.gender = data.get('gender')
        self.occupation = data.get('occupation')
        self.preferred_gender = data.get('preferred_gender')
        self.city = data.get('city')
        self.state = data.get('state')
        self.dob = data.get('dob')

        self.bio = data.get("bio")
        self.height_ft_max = data.get("height_ft_max")
        self.height_ft_min = data.get("height_ft_min")
        self.height_inch_min = data.get("height_inch_min")
        self.height_inch_max = data.get("height_inch_max")
        self.education = data.get("education")

        self.preferred_education = data.get("preferred_education")
        self.preferred_location = data.get("preferred_location")
        self.preferred_race = data.get("preferred_race")
        self.preferred_religion = data.get("preferred_religion")
        self.budget_range = data.get("budget_range")
        self.active_hour = data.get("active_hour")
        self.proximity_range = data.get("proximity_range")

        # self.prompts = data.prompts

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        # for key, item in data.items():
        #     print(key, item)
        #     setattr(self, key, item)
        # self.modified_at = datetime.datetime.utcnow()
        # db.session.commit()

        rdata = dict(data)
        user_id = rdata['id']
        instance = user_simpleton.query.filter(user_simpleton.id == user_id)
        data = instance.update(dict(rdata))
        db.session.commit()
        updateddata = instance.first()
        return updateddata

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return user_simpleton.query.all()

    @staticmethod
    def get_one_user(id):
        return user_simpleton.query.get(id)

    @staticmethod
    def get_user_by_email(value):
        return user_simpleton.query.filter_by(email=value).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'gender': self.gender,
            'occupation': self.occupation,
            'preferred_gender': self.preferred_gender,
            'city': self.city,
            'state': self.state,
            'dob': self.dob,
            'bio': self.bio,
            'height_ft_max': self.height_ft_max,
            'height_ft_min': self.height_ft_min,
            'height_inch_min': self.height_inch_min,
            'height_inch_max': self.height_inch_max,
            'education': self.education,
            'preferred_education': self.preferred_education,
            'preferred_location': self.preferred_location,
            'preferred_race': self.preferred_race,
            'preferred_religion': self.preferred_religion,
            'budget_range': self.budget_range,
            'active_hour': self.active_hour,
            'proximity_range': self.proximity_range,

        }




class user_simpleton_schema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Int(required=True)
    gender = fields.Str(required=False)
    occupation = fields.Str(required=False)
    preferred_gender = fields.Str(required=False)
    city = fields.Str(required=False)
    state = fields.Str(required=False)
    dob = fields.Str(required=False)

    bio = fields.Str(required=False)
    height_ft_max = fields.Integer(required=False)
    height_ft_min = fields.Integer(required=False)
    height_inch_min = fields.Integer(required=False)
    height_inch_max = fields.Integer(required=False)
    education = fields.Str(required=False)

    preferred_education = fields.Str(required=False)
    preferred_location = fields.Str(required=False)
    preferred_race = fields.Str(required=False)
    preferred_religion = fields.Str(required=False)
    budget_range = fields.Str(required=False)
    active_hour = fields.Str(required=False)
    proximity_range = fields.Str(required=False)



