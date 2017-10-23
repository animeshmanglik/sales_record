#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class Account(db.Model):
    __tablename__ = 'account'

    uuid = db.Column(db.String, primary_key=True)
    is_dealer = db.Column(db.Boolean)
    created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, uuid, is_dealer):
        self.uuid = uuid
        self.is_dealer = is_dealer

    def create(self):
        db.session.add(self)
        return self


class AccountSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Account
        sqla_session = db.session

    uuid = fields.String(required=True)
    is_dealer = fields.Boolean()
