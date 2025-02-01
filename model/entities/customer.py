from sqlalchemy import Column, Integer, String, Boolean

from configuration.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    deleted = Column(Boolean, default=False)
