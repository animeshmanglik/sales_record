#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class Dealership(db.Model):
    __tablename__ = 'dealership'

    uuid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, uuid, name, location):
        self.uuid = uuid
        self.name = name
        self.location = location

    def create(self):
        db.session.add(self)
        return self


class DealershipSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Dealership
        sqla_session = db.session

    uuid = fields.String(required=True)
    name = fields.String(required=True)
    location = fields.String(required=True)
