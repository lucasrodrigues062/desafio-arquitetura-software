from fastapi import HTTPException
from sqlmodel  import Session
from configuration.database import get_db, engine
from controller.schemas.customer import *
from model.entities.customer import Customer

def create_customer(cliente: CustomerCreate):
    with Session(engine) as db:
        db_cliente = Customer(name=cliente.name, email=cliente.email, phone_number=cliente.phone_number, address=cliente.address)
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

def update_customer(cliente: CustomerUpdate, customer_id: int):
    with Session(engine) as db:
        customer = db.get(Customer, customer_id)
        if not customer or customer.deleted == True:
            raise HTTPException(status_code=404, detail="Customer not found")
        if cliente.address is not None:
            customer.address = cliente.address
        if cliente.phone_number is not None:
            customer.phone_number = cliente.phone_number
        if cliente.name is not None:
            customer.name = cliente.name
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

def get_customer_by_id(customer_id: int):
    with Session(engine) as db:
        customer = db.get(Customer, customer_id)
        if not customer or customer.deleted == True:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

def get_customers():
    with Session(engine) as db:
        customers = db.query(Customer).filter(Customer.deleted == False).all()
        return customers

def count_customers():
    with Session(engine) as db:
        customers = db.query(Customer).filter(Customer.deleted == False).all()
        print(len(customers))
        return CustomerCount(customers_quantity=len(customers))

def get_customer_by_name(name: str):
    with Session(engine) as db:
        customer = db.query(Customer).filter(Customer.name == name).filter(Customer.deleted == False).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer

def delete_customer(customer_id: int):
    with Session(engine) as db:
        customer = db.get(Customer,customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        customer.deleted = True
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return