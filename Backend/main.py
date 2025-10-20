from fastapi import FastAPI
from . import models, database
from .routers import users, transactions

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="FinTech Fraud Detection API")

app.include_router(users.router)
app.include_router(transactions.router)