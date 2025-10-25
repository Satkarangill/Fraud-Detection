from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.core.database import get_db
from Backend.table_models.budget_model import BudgetTable as Budget

router = APIRouter(prefix="/budgets", tags=["Budgets"])

# Create budget
@router.post("/")
def create_budget(user_id: int, category: str, amount: float, db: Session = Depends(get_db)):
    budget = Budget(user_id=user_id, category=category, amount=amount)
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return {"id": budget.id, "user_id": budget.user_id, "category": budget.category, "amount": budget.amount}

# Get all budgets
@router.get("/")
def get_budgets(db: Session = Depends(get_db)):
    return db.query(Budget).all()
