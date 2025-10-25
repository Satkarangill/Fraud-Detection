from fastapi import FastAPI
from Backend.core.database import engine
from Backend.table_models.user_model import User as UserBase
from Backend.table_models.transaction_model import Transaction as TransactionBase
from Backend.table_models.budget_model import BudgetTable as BudgetBase
from Backend.routes import user_routes, transaction_routes, budget_routes

# Initialize database tables (if not already created)
UserBase.metadata.create_all(bind=engine)
TransactionBase.metadata.create_all(bind=engine)
BudgetBase.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Fraud Detection API")

# Include routes
app.include_router(user_routes.router)
app.include_router(transaction_routes.router)
app.include_router(budget_routes.router)



