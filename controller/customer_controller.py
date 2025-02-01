from fastapi import APIRouter, status

from model.services.customer_service import *

customer_router = APIRouter()


@customer_router.post('/api/v1/customers', tags=["customer"],  status_code=status.HTTP_201_CREATED, include_in_schema=True, response_model=CustomerView)
def create(customer: CustomerCreate):
    return create_customer(customer)

@customer_router.patch('/api/v1/customers/{customer_id}', tags=["customer"],  status_code=status.HTTP_200_OK, include_in_schema=True, response_model=CustomerView)
def update(customer_id: int, customer: CustomerUpdate):
    return update_customer(customer, customer_id)


@customer_router.get('/api/v1/customers/{customer_id}', tags=["customer"],  status_code=status.HTTP_200_OK, include_in_schema=True, response_model=CustomerView)
def update(customer_id: int):
    return get_customer_by_id(customer_id)

@customer_router.get('/api/v1/customers', tags=["customer"],  status_code=status.HTTP_200_OK, include_in_schema=True, response_model=list[CustomerView])
def update(name: str | None = None):
    if name is not None:
        return get_customer_by_name(name)
    return get_customers()

@customer_router.get('/api/v1/count/customers', tags=["customer"],  status_code=status.HTTP_200_OK, include_in_schema=True, response_model=CustomerCount )
def count():
    return count_customers()