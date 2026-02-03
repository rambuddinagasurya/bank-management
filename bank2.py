import mysql.connector as db
import random
from datetime import datetime
from decimal import Decimal

# ----------------- Database Connection -----------------
conn=db.connect(
    host="localhost",
    user="root",
    password="Nsurya@321",
    database="bank_new")

cursor = conn.cursor()

# ----------------- Step 1: Registration -----------------
def register_user():
    print("\n=== User Registration ===")
    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")
    pin = int(input("Set a 4-digit PIN: "))
    account_type = input("Account type (savings/current): ")

    account_no = random.randint(1000000000, 9999999999)
    balance = Decimal('0.0')

    # Insert into users table
    user_query = "INSERT INTO users (name, phone, account_no, pin) VALUES (%s, %s, %s, %s)"
    cursor.execute(user_query, (name, phone, account_no, pin))

    # Insert into accounts table
    account_query = "INSERT INTO accounts (account_no, account_type, balance) VALUES (%s, %s, %s)"
    cursor.execute(account_query, (account_no, account_type, balance))

    conn.commit()
    print("\n✅ Account created successfully!")
    print("Your Account Number is:", account_no)

# ----------------- Step 2: Login -----------------
def login_user():
    print("\n=== User Login ===")
    account_no = int(input("Enter your account number: "))
    pin = int(input("Enter your 4-digit PIN: "))

    query = "SELECT * FROM users WHERE account_no=%s AND pin=%s"
    cursor.execute(query, (account_no, pin))
    result = cursor.fetchone()

    if result:
        print("\n✅ Login Successful!")
        print(f"Welcome, {result[1]}")  # result[1] = name
        return account_no
    else:
        print("\n❌ Invalid Account Number or PIN")
        return None

# ----------------- Step 3: Transactions -----------------
def perform_transactions(account_no):
    while True:
        print("\n=== Transaction Menu ===")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        # Fetch current balance
        cursor.execute("SELECT balance FROM accounts WHERE account_no=%s", (account_no,))
        balance = cursor.fetchone()[0]  # Decimal type from MySQL

        if choice == '1':
            # Deposit
            amount = Decimal(input("Enter amount to deposit: "))
            balance += amount
            cursor.execute("UPDATE accounts SET balance=%s WHERE account_no=%s", (balance, account_no))
            cursor.execute(
                "INSERT INTO transactions (account_no, type, amount, date) VALUES (%s, %s, %s, %s)",
                (account_no, 'Deposit', amount, datetime.now())
            )
            conn.commit()
            print(f"✅ Amount deposited successfully! New Balance: {balance}")

        elif choice == '2':
            # Withdraw
            amount = Decimal(input("Enter amount to withdraw: "))
            if amount > balance:
                print("❌ Insufficient balance!")
            else:
                balance -= amount
                cursor.execute("UPDATE accounts SET balance=%s WHERE account_no=%s", (balance, account_no))
                cursor.execute(
                    "INSERT INTO transactions (account_no, type, amount, date) VALUES (%s, %s, %s, %s)",
                    (account_no, 'Withdraw', amount, datetime.now())
                )
                conn.commit()
                print(f"✅ Amount withdrawn successfully! New Balance: {balance}")

        elif choice == '3':
            # Check Balance
            print(f"💰 Your current balance is: {balance}")

        elif choice == '4':
            # Transaction History
            cursor.execute(
                "SELECT type, amount, date FROM transactions WHERE account_no=%s ORDER BY date DESC",
                (account_no,)
            )
            records = cursor.fetchall()
            if not records:
                print("No transactions yet.")
            else:
                print("\n=== Transaction History ===")
                for r in records:
                    print(f"{r[2]} | {r[0]} | Amount: {r[1]}")

        elif choice == '5':
            print("Exiting... Thank you!")
            break

        else:
            print("❌ Invalid choice. Try again.")

# ----------------- Main Program -----------------
while True:
    print("\n=== Welcome to Python Bank ===")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    option = input("Choose an option (1-3): ")

    if option == '1':
        register_user()
    elif option == '2':
        acc_no = login_user()
        if acc_no:
            perform_transactions(acc_no)
    elif option == '3':
        print("Goodbye!")
        break
    else:
        print("❌ Invalid option. Try again.")

# ----------------- Close Connection -----------------
cursor.close()
conn.close()
conn.close()
