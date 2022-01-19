from fastapi import FastAPI, status, HTTPException

# Both used for BaseModel
from pydantic import BaseModel
from typing import Optional

# You need this to be able to turn classes into JSONs and return
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

class Customer(BaseModel):
    customer_id: str
    country:str

class URLLink(BaseModel):
    url: Optional[str] = None

class Invoice(BaseModel):
    invoice_no: int
    invoice_date: str
    customer: Optional[URLLink] = None
 
fakeInvoiceTable = dict()

# This is important for general execution and the docker later
app = FastAPI()

# Base URL
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Add a new Customer
@app.post("/customer")
async def create_customer(item: Customer): # body awaits a json with customer info
# This is how to work with and return an item
#   country = item.country
#   return {item.country}

    # Encode the created customer item if successful into a JSON and return it to the client with 201
    json_compatible_item_data = jsonable_encoder(item)
    return JSONResponse(content=json_compatible_item_data, status_code=201)

@app.get("/customer/{customer_id}") # Customer ID will be a path parameter
async def read_customer(customer_id: str):

    # Dummy values
    # Only succeed if the item is 12345
    if customer_id == "12345":
        # Create a fake customer
        item = Customer(customer_id="12345", country="Germany")

        # Encode the customer into JSON and send it back
        json_compatible_item_data =jsonable_encoder(item)
        return JSONResponse(content=json_compatible_item_data)
    else:
        # Raise a 404 exception
        raise HTTPException(status_code=404, detail="Item not found")

# Create new invoice for a customer
@app.post("/customer/{customer_id}/invoice")
async def create_invoice(customer_id: str, invoice: Invoice):

    # Add the customer link to the invoice
    invoice.customer.url = "/customer/" + customer_id

    # Turn the invoice instance into a JSON string and store it
    jsonInvoice = jsonable_encoder(invoice)
    fakeInvoiceTable[invoice.invoice_no] = jsonInvoice

    # Read it from the store and return the stored item
    ex_invoice = fakeInvoiceTable[invoice.invoice_no]

    return JSONResponse(content=ex_invoice)

# Return all invoices for a customer
@app.get("/customer/{customer_id}/invoice")
async def get_invoices(customer_id: str):

    # Creat links to the actual invoice (get from DB)
    ex_json = {"id_12345": "/invoice/12345",
               "id_78910": "/invoice/78910"
               }
    return JSONResponse(content=ex_json)

# Return a specific invoice
@app.get("/invoice/{invoice_no}")
async def read_invoice(invoice_no: int):
    
    # Read invoice from the dictionary
    ex_invoice = fakeInvoiceTable[invoice_no]

    # Return the JSON that we stored
    return JSONResponse(content=ex_invoice)

#Get a specific stock code on the invoice
@app.get("/invoice/{invoice_no}/{stockcode}/")
async def read_item(invoice_no: int, stockcode: str):
    return {"message": "Hello World"}

# Add a stockcode to the invoice
@app.post("/invoice/{invoice_no}/{stockcode}/")
async def add_item(invoice_no: int, stockcode: str):
    return {"message": "Hello World"}