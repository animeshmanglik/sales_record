# QUESTIONS README

Upload file
`api/v1/sale?file=true`

---
Latest sales price of a specific vehicle (i.e. sales price by VIN)
`/api/v1/sale?vin=2A8HR64X38R787250`

Returns the sales record.
Client can massage the sale price out of the result object.
If data being sent across network isn't that large, I believe in sending the
sale record, rather than just the sale price(disables the flexibility of API)

---
Historical sales price of a class of vehicles (i.e. sales price by Make/Model/Year)
`/api/v1/sale/vehicle?make=audi`

`/api/v1/sale/vehicle?model=a4`

`/api/v1/sale/vehicle?year=2011`

---
Transaction history for a specific dealership
`/api/v1/sale/dealership?name=bmw`

`/api/v1/sale/dealership?location=thousand oaks`

`/api/v1/sale/dealership?name=bmw&location=thousand oaks`

---
---
Security - How would you protect against outsiders from inserting/querying records?
Ways I think API could be protected
1. Have JSONWebToken to verify if the user is authorized.
2. Have Entitlements table to verify the user has access.
3. Have API Secret Key sent as header.

---
Scalability - Would anything change if your system had 100 million vehicle sale records? What if the API had to handle 10 searches per second?
1. Have multithreading to read data, a general idea would be to have 10 threads to load balance request.
2. Have master/ slave system where reads are made from slave.

---
Data Integrity - How would you handle erroneous sale records data (e.g. malformed VINs, invalid field values)?
1. We could have a database to check against values, for ex. Make, Model, Year could be checked against these.
2. Vins can be checked with regexes.
3. A proper database schema would ensure against inconsistent values.
4. Avoid as much as manual entry.

---
Auditability - How would you track the source of any incoming data as well as the source of any searches?
1. One way would be to track the IPs of the client.
2. You could add query params to specifically know from where the source is coming(helpful in analytics)

---
