from pydantic import BaseModel, EmailStr
from typing import Optional

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: str
    phone_number: Optional[str] = None
    address: Optional[str] = None

class CustomerCount(BaseModel):
    customers_quantity: int

class CustomerView(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: Optional[str] = None
    address: Optional[str] = None