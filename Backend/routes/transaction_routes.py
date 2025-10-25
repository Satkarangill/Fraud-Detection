from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from table_models.transaction_model import Transaction as TransactionTable

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# Create transaction
@router.post("/")
def create_transaction(sender_id: int, receiver_id: int, amount: float, db: Session = Depends(get_db)):
    txn = TransactionTable(sender_id=sender_id, receiver_id=receiver_id, amount=amount)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return {"id": txn.id, "amount": txn.amount, "sender_id": txn.sender_id, "receiver_id": txn.receiver_id}

# Get all transactions
@router.get("/")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(TransactionTable).all()
