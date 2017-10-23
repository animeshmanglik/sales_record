#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    vin = db.Column(db.String, primary_key=True)
    make = db.Column(db.String)
    model = db.Column(db.String)
    year = db.Column(db.Integer)
    created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, vin, make, model, year):
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year

    def create(self):
        db.session.add(self)
        return self


class VehicleSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Vehicle
        sqla_session = db.session

    vin = fields.String(required=True)
    make = fields.String(required=True)
    model = fields.String(required=True)
    year = fields.Number(required=True)
