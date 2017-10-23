#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class Person(db.Model):
    __tablename__ = 'person'

    uuid = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, uuid, first_name, last_name):
        self.uuid = uuid
        self.first_name = first_name
        self.last_name = last_name

    def create(self):
        db.session.add(self)
        return self


class PersonSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Person
        sqla_session = db.session

    uuid = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
