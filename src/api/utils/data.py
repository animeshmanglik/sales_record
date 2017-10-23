import uuid
from api.models.model_vehicle import Vehicle, VehicleSchema
from api.models.model_dealership import Dealership, DealershipSchema
from api.models.model_person import Person, PersonSchema
from api.models.model_sale import Sale, SaleSchema
from api.models.model_account import Account, AccountSchema


def add_vehicle_record(data):
    vehicle_schema = VehicleSchema()
    vehicle, error = vehicle_schema.load(data)
    result = vehicle_schema.dump(vehicle.create()).data
    return result


def add_delearship_record(data):
    account_id = str(uuid.uuid4())
    account_data = {
        "uuid": account_id,
        "is_dealer": True
    }
    data["uuid"] = account_id
    add_account_record(account_data)

    dealership_schema = DealershipSchema()
    dealership, error = dealership_schema.load(data)
    result = dealership_schema.dump(dealership.create()).data
    return result


def add_person_record(data):
    account_id = str(uuid.uuid4())
    account_data = {
        "uuid": account_id,
        "is_dealer": False
    }
    data["uuid"] = account_id
    add_account_record(account_data)

    person_schema = PersonSchema()
    person, error = person_schema.load(data)
    result = person_schema.dump(person.create()).data
    return result


def add_account_record(data):
    account_schema = AccountSchema()
    account, error = account_schema.load(data)
    result = account_schema.dump(account.create()).data
    return result


def add_dealer_person(data):
    if data["type"] == "dealership":
        return add_delearship_record(data)
    elif data["type"] == "person":
        return add_person_record(data)


def add_sale_record(data):
    sale_schema = SaleSchema()
    sale, error = sale_schema.load(data)
    result = sale_schema.dump(sale.create()).data
    return result


def add_sales(data):
    vehicle_data = data["vehicle"]
    buyer_data = data["buyer"]
    seller_data = data["seller"]

    vehicle = add_vehicle_record(vehicle_data)

    buyer = add_dealer_person(buyer_data)

    seller = add_dealer_person(seller_data)

    sale_record = {}
    sale_record["vin"] = vehicle_data["vin"]
    sale_record["buyer"] = buyer["uuid"]
    sale_record["seller"] = seller["uuid"]
    sale_record["price"] = data["price"]
    sale_record["transaction_date"] = data["transaction_date"]

    return add_sale_record(sale_record)

def delete_all_records():
    fetched = Sale.query.delete()
    fetched = Account.query.delete()
    fetched = Vehicle.query.delete()
    fetched = Dealership.query.delete()
    fetched = Person.query.delete()

    return True
