# Interactive Database Explorer
import os
from Backend.core.database import SessionLocal
from table_models.budget_model import BudgetTable
from table_models.user_model import User
from table_models.transaction_model import Transaction
from sqlalchemy import text

def show_menu():
    print("\n" + "="*50)
    print("    FRAUD DETECTION DATABASE EXPLORER")
    print("="*50)
    print("1. View all users")
    print("2. View all transactions")
    print("3. Search user by email")
    print("4. View transactions by user")
    print("5. Add new user")
    print("6. Add new transaction")
    print("7. Database statistics")
    print("8. Run custom SQL query")
    print("9. Exit")
    print("="*50)

def view_all_users():
    db = SessionLocal()
    users = db.query(User).all()
    print(f"\n--- ALL USERS ({len(users)} total) ---")
    for user in users:
        print(f"ID: {user.id} | Email: {user.email} | Balance: ${user.balance} | Active: {user.is_active}")
    db.close()

def view_all_transactions():
    db = SessionLocal()
    transactions = db.query(Transaction).all()
    print(f"\n--- ALL TRANSACTIONS ({len(transactions)} total) ---")
    for txn in transactions:
        print(f"ID: {txn.id} | Amount: ${txn.amount} | From: {txn.sender_id} | To: {txn.receiver_id} | Time: {txn.timestamp}")
    db.close()

def search_user_by_email():
    email = input("Enter email to search: ")
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if user:
        print(f"\n--- USER FOUND ---")
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Balance: ${user.balance}")
        print(f"Active: {user.is_active}")
    else:
        print(f"\nUser with email '{email}' not found.")
    db.close()

def view_transactions_by_user():
    user_id = input("Enter user ID: ")
    try:
        user_id = int(user_id)
        db = SessionLocal()
        transactions = db.query(Transaction).filter(Transaction.sender_id == user_id).all()
        print(f"\n--- TRANSACTIONS FOR USER {user_id} ({len(transactions)} total) ---")
        for txn in transactions:
            print(f"ID: {txn.id} | Amount: ${txn.amount} | To: {txn.receiver_id} | Time: {txn.timestamp}")
        db.close()
    except ValueError:
        print("Invalid user ID. Please enter a number.")

def add_new_user():
    email = input("Enter email: ")
    password = input("Enter password: ")
    balance = input("Enter initial balance (default 0): ")
    balance = float(balance) if balance else 0.0
    
    db = SessionLocal()
    try:
        new_user = User(
            email=email,
            hashed_password=password,
            balance=balance
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"\n[SUCCESS] Created user: {new_user.email} (ID: {new_user.id})")
    except Exception as e:
        print(f"[ERROR] Failed to create user: {e}")
    finally:
        db.close()

def add_new_transaction():
    sender_id = input("Enter sender ID: ")
    receiver_id = input("Enter receiver ID: ")
    amount = input("Enter amount: ")
    
    try:
        sender_id = int(sender_id)
        receiver_id = int(receiver_id)
        amount = float(amount)
        
        db = SessionLocal()
        sender = db.query(User).filter(User.id == sender_id).first()
        if not sender:
            print(f"[ERROR] Sender with ID {sender_id} not found.")
            db.close()
            return
            
        new_transaction = Transaction(
            amount=amount,
            sender_id=sender_id,
            receiver_id=receiver_id,
            user=sender
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)
        print(f"\n[SUCCESS] Created transaction: ${new_transaction.amount} (ID: {new_transaction.id})")
        db.close()
    except ValueError:
        print("[ERROR] Invalid input. Please enter numbers for IDs and amount.")
    except Exception as e:
        print(f"[ERROR] Failed to create transaction: {e}")

def database_statistics():
    db = SessionLocal()
    
    # User stats
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_balance = db.query(User).with_entities(User.balance).all()
    total_balance = sum([user.balance for user in total_balance])
    
    # Transaction stats
    total_transactions = db.query(Transaction).count()
    total_amount = db.query(Transaction).with_entities(Transaction.amount).all()
    total_amount = sum([txn.amount for txn in total_amount])
    
    print(f"\n--- DATABASE STATISTICS ---")
    print(f"Total Users: {total_users}")
    print(f"Active Users: {active_users}")
    print(f"Total User Balance: ${total_balance}")
    print(f"Total Transactions: {total_transactions}")
    print(f"Total Transaction Amount: ${total_amount}")
    
    db.close()

def run_custom_sql():
    query = input("Enter SQL query: ")
    db = SessionLocal()
    try:
        result = db.execute(text(query))
        rows = result.fetchall()
        print(f"\n--- QUERY RESULTS ({len(rows)} rows) ---")
        for row in rows:
            print(row)
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")
    finally:
        db.close()

def main():
    print("Welcome to the Fraud Detection Database Explorer!")
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'database.db')
    print(f"Database file: {db_path}")
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-9): ")
        
        if choice == "1":
            view_all_users()
        elif choice == "2":
            view_all_transactions()
        elif choice == "3":
            search_user_by_email()
        elif choice == "4":
            view_transactions_by_user()
        elif choice == "5":
            add_new_user()
        elif choice == "6":
            add_new_transaction()
        elif choice == "7":
            database_statistics()
        elif choice == "8":
            run_custom_sql()
        elif choice == "9":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
