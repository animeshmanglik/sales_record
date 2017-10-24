#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from flask import Blueprint
from flask import request
from flask import jsonify
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.data import add_sales, delete_all_records, add_vehicle_record
from api.utils.database import db
from api.models.model_sale import Sale, SaleSchema
from api.models.model_vehicle import Vehicle, VehicleSchema
from api.models.model_dealership import Dealership, DealershipSchema
from api.models.model_person import Person, PersonSchema
from api.models.model_account import Account, AccountSchema


route_path_general = Blueprint("route_path_general", __name__)
sale_schema = SaleSchema(many=True, exclude=['id', 'created'])


@route_path_general.route('/sale', methods=['GET'])
def get_sales_record():
    """Get all sales Records
    Returns Sales object
    """
    query_params = request.args
    sales = []
    try:
        if query_params.get('vin'):
            vin = query_params.get('vin')
            sale_query = Sale.query \
                        .filter_by(vin=vin) \
                        .order_by('transaction_date desc') \
                        .limit(1)
        else:
            sale_query = Sale.query.all()
        sales, error = sale_schema.dump(sale_query)
        return response_with(resp.SUCCESS_200, value={"sales": sales})
    except Exception:
        return response_with(resp.BAD_REQUEST_400)


@route_path_general.route('/sale', methods=['POST'])
def create_sale_record():
    """Create sales Records
    Input could be a single Record or a file upload
    Returns Sales object
    """
    query_params = request.args
    result = []
    try:
        if query_params.get('file'):
            file = request.files['file']
            file.seek(0)
            sale_records = json.loads(file.read())
            for sale_record in sale_records:
                result.append(add_sales(sale_record))
        else:
            data = request.get_json()
            result = add_sales(data)
        db.session.commit()
        return response_with(resp.SUCCESS_200, value={"sale": result})
    except Exception as e:
        db.session.rollback()
        return response_with(resp.BAD_REQUEST_400)


@route_path_general.route('/sale/vehicle', methods=['GET'])
def get_sales_record_by_vehicle():
    """Get all sales Records based on a vehicle make, model, year
    Returns Sales object
    """
    query_params = request.args
    sales = []
    vehicle_filter = {}
    vehicle_schema = VehicleSchema(many=True, only=['vin'])

    if query_params.get('make'):
        make = query_params.get('make')
        vehicle_filter["make"] = make
    if query_params.get('model'):
        model = query_params.get('model')
        vehicle_filter["model"] = model
    if query_params.get('year'):
        year = query_params.get('year')
        vehicle_filter["year"] = year

    try:
        if len(vehicle_filter):
            vehicle_query = Vehicle.query.filter_by(**vehicle_filter)
            vehicles, error = vehicle_schema.dump(vehicle_query)

            vehicle_id = [vehicle['vin'] for (vehicle) in vehicles]

            if len(vehicle_id):
                sale_query = Sale.query.filter(Sale.vin.in_(vehicle_id)).all()
                sales, error = sale_schema.dump(sale_query)

        return response_with(resp.SUCCESS_200, value={"sales": sales})
    except Exception:
        return response_with(resp.BAD_REQUEST_400)


@route_path_general.route('/sale/dealership', methods=['GET'])
def get_sales_record_by_dealership():
    """Get all sales Records based on a particular dealership
    Returns Sales object
    """
    query_params = request.args
    dealership_filter = {}
    sales = []
    if query_params.get('name'):
        name = query_params.get('name')
        dealership_filter["name"] = name
    if query_params.get('location'):
        location = query_params.get('location')
        dealership_filter["location"] = location

    try:
        if len(dealership_filter):
            dealership = query_params.get('dealership')
            dealership_query = Dealership.query.filter_by(**dealership_filter)
            dealership_schema = DealershipSchema(many=True, only=['uuid'])
            dealerships, error = dealership_schema.dump(dealership_query)

            dealership_id = [dealership['uuid'] for (dealership) in dealerships]

            if len(dealership_id):
                sale_buyer_query = Sale \
                                    .query \
                                    .filter \
                                    (Sale.buyer.in_(dealership_id)).all()
                sale_seller_query = Sale \
                                    .query \
                                    .filter \
                                    (Sale.seller.in_(dealership_id)).all()

                combined_query = sale_buyer_query.extend(sale_seller_query)
                sales, error = sale_schema.dump(sale_buyer_query)

        return response_with(resp.SUCCESS_200, value={"sales": sales})
    except Exception as e:
        print e
        return response_with(resp.BAD_REQUEST_400)


@route_path_general.route('/vehicle', methods=['GET'])
def get_vehicles_record():
    """Get all vehicle Records
    Returns Vehicle object
    """
    fetched = Vehicle.query.all()
    vehicle_schema = VehicleSchema(many=True, exclude=['created'])
    vehicles, error = vehicle_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"vehicles": vehicles})


@route_path_general.route('/vehicle', methods=['POST'])
def create_vehicles_record():
    """Get all vehicle Records
    Returns Vehicle object
    """
    query_params = request.args
    result = []
    try:
        data = request.get_json()
        result = add_vehicle_record(data)
        db.session.commit()
        return response_with(resp.SUCCESS_200, value={"vehicle": result})
    except Exception as e:
        db.session.rollback()
        return response_with(resp.BAD_REQUEST_400)


@route_path_general.route('/dealership', methods=['GET'])
def get_dealerships_record():
    """Get all dealership Records
    Returns Dealership object
    """
    dealership_query = Dealership.query.all()
    dealership_schema = DealershipSchema(many=True, exclude=['created'])
    dealerships, error = dealership_schema.dump(dealership_query)
    return response_with(resp.SUCCESS_200, value={"dealerships": dealerships})


@route_path_general.route('/person', methods=['GET'])
def get_persons_record():
    """Get all person Records
    Returns Person object
    """
    fetched = Person.query.all()
    person_schema = PersonSchema(many=True, exclude=['created'])
    persons, error = person_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"persons": persons})


@route_path_general.route('/account', methods=['GET'])
def get_accounts_record():
    """Get all account Records
    Returns Account object
    """
    fetched = Account.query.all()
    account_schema = AccountSchema(many=True, exclude=['created'])
    accounts, error = account_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"accounts": accounts})


@route_path_general.route('/clear', methods=['DELETE'])
def get_clear_record():
    """Remove all the entries in the db
    Returns an empty object
    """
    try:
        did_delete = delete_all_records()
        return response_with(resp.SUCCESS_200, value={"deleted": did_delete})
    except Exception:
        return response_with(resp.SERVER_ERROR_500)
