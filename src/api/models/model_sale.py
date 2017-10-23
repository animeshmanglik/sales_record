#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class Sale(db.Model):
    __tablename__ = 'sale'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vin = db.Column(db.String, db.ForeignKey('vehicle.vin'))
    buyer = db.Column(db.String, db.ForeignKey('account.uuid'))
    seller = db.Column(db.String, db.ForeignKey('account.uuid'))
    price = db.Column(db.Integer)
    transaction_date = db.Column(db.DateTime)
    created = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, vin, buyer, seller, price, transaction_date):
        self.vin = vin
        self.buyer = buyer
        self.seller = seller
        self.price = price
        self.transaction_date = transaction_date

    def create(self):
        db.session.add(self)
        return self


class SaleSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Sale
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    vin = fields.String(required=True)
    buyer = fields.String(required=True)
    seller = fields.String(required=True)
    price = fields.Integer(required=True)
    transaction_date = fields.DateTime(required=True)
