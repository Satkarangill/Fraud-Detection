# Simple database test script
from database import SessionLocal, engine
from models import User, Transaction
from sqlalchemy import text

print("=== Database Connection Test ===")

# Test 1: Check if database file exists and is accessible
try:
    db = SessionLocal()
    result = db.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
    tables = result.fetchall()
    print(f"[SUCCESS] Database connected successfully!")
    print(f"[INFO] Found {len(tables)} tables: {[table[0] for table in tables]}")
    db.close()
except Exception as e:
    print(f"[ERROR] Database connection failed: {e}")
    exit(1)

print("\n=== Table Structure Test ===")

# Test 2: Check table structure
try:
    db = SessionLocal()
    
    # Check users table
    result = db.execute(text("PRAGMA table_info(users);"))
    users_columns = result.fetchall()
    print(f"[INFO] Users table has {len(users_columns)} columns:")
    for col in users_columns:
        print(f"   - {col[1]} ({col[2]})")
    
    # Check transactions table
    result = db.execute(text("PRAGMA table_info(transactions);"))
    transactions_columns = result.fetchall()
    print(f"[INFO] Transactions table has {len(transactions_columns)} columns:")
    for col in transactions_columns:
        print(f"   - {col[1]} ({col[2]})")
    
    db.close()
except Exception as e:
    print(f"[ERROR] Table structure check failed: {e}")

print("\n=== Data Operations Test ===")

# Test 3: Test basic CRUD operations
try:
    db = SessionLocal()
    
    # Count existing records
    user_count = db.query(User).count()
    transaction_count = db.query(Transaction).count()
    print(f"[INFO] Current data:")
    print(f"   - Users: {user_count}")
    print(f"   - Transactions: {transaction_count}")
    
    # Try to add a new user with unique email
    import time
    unique_email = f"test_user_{int(time.time())}@example.com"
    
    new_user = User(
        email=unique_email,
        hashed_password="test_password_123",
        balance=100.0
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(f"[SUCCESS] Created new user: {new_user.email} (ID: {new_user.id})")
    
    # Add a transaction for this user
    new_transaction = Transaction(
        amount=25.50,
        sender_id=new_user.id,
        receiver_id=999,  # Some other user ID
        user=new_user
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    print(f"[SUCCESS] Created new transaction: ${new_transaction.amount} (ID: {new_transaction.id})")
    
    # Query the data back
    retrieved_user = db.query(User).filter(User.email == unique_email).first()
    retrieved_transaction = db.query(Transaction).filter(Transaction.id == new_transaction.id).first()
    
    print(f"[SUCCESS] Retrieved user: {retrieved_user.email}, Balance: ${retrieved_user.balance}")
    print(f"[SUCCESS] Retrieved transaction: ${retrieved_transaction.amount}, Sender: {retrieved_transaction.sender_id}")
    
    db.close()
    print("\n[SUCCESS] All database tests passed successfully!")
    
except Exception as e:
    print(f"[ERROR] Data operations test failed: {e}")
    db.close()
