from marshmallow import fields, Schema

from models.user_simpleton import user_simpleton
from . import db


class prompt(db.Model):
    prompt_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_simpleton.id'))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data, name, user_id, item, prompt_id):
        rdata = dict(data["prompts"][item])
        instance = prompt.query.filter(prompt.prompt_id == prompt_id)
        udata = instance.update(dict(rdata))
        db.session.commit()
        updateddata = instance.first()
        return updateddata

    @staticmethod
    def get_prompts_by_user(user_id):
        prompts = user_simpleton.get_one_user(user_id).prompts
        return prompts

    @staticmethod
    def get_one_prompt(id):
        return prompt.query.get(id)

    def to_json(self):
        return {
            "prompt_id":self.prompt_id,
            "name": self.name,
            "user_id": self.user_id
        }
    def dump_prompt(self):
        return {"prompts": {'prompt_id': self.prompt_id,
                               'name': self.name,
                               'user_id': self.user_id
                               }}


class prompt_schema(Schema):
    prompt_id = fields.Int(required=True)
    name = fields.Str(required=False)
    user_id = fields.Str(required=False)
