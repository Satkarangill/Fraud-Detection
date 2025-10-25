from database import Base, engine
# import the actual model class names used in the model files
from table_models.user_model import User
from table_models.transaction_model import Transaction
from table_models.budget_model import BudgetTable

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done ✅")
