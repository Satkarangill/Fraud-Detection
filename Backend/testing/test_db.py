from Backend.core.database import SessionLocal, engine
from Backend.table_models import Base
from Backend.table_models.transaction_model import Transaction
from Backend.table_models.user_model import User
from Backend.table_models.budget_model import BudgetTable


# Force reset tables before testing
print("🔄 Dropping all existing tables...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Tables recreated.\n")

db = SessionLocal()

# Use unique test data each run
user1 = User(email="alice@example.com", hashed_password="hashed123")
user2 = User(email="bob@example.com", hashed_password="bobpass")

# Insert only if not already present (extra safety)
for user in [user1, user2]:
    existing = db.query(User).filter_by(email=user.email).first()
    if not existing:
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"🧍 Added {user.email}")
    else:
        print(f"⚠️ {user.email} already exists, skipping")

#  Add test transactions
txn1 = Transaction(amount=50.0, sender_id=user1.id, receiver_id=user2.id, user=user1)
txn2 = Transaction(amount=100.0, sender_id=user2.id, receiver_id=user1.id, user=user2)
db.add_all([txn1, txn2])
db.commit()

print("\n📋 Users:")
for u in db.query(User).all():
    print(f" - {u.id}: {u.email}")

print("\n📋 Transactions:")
for t in db.query(Transaction).all():
    print(f" - {t.id}: {t.amount} from {t.sender_id} → {t.receiver_id}")

print("\n📋 Budgets (should be empty):")
for b in db.query(BudgetTable).all():
    print(f" - {b.id}: {b.category} limit {b.limit} spent {b.spent}")

db.close()
print("\n All test cases ran successfully.")
