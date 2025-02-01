from fastapi import FastAPI
from controller.customer_controller import customer_router
from configuration.database import Base, engine, SessionLocal, create_db_and_tables

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
app.include_router(customer_router)