#USING CLASS METHOD

#This program allows users to create accounts, authenticate, and perform banking operations. 
#It saves transactions to a JSON file for each customer.

# add this to github


import json
import os
from getpass import getpass
from datetime import datetime


# Class
class Customer:
    def __init__(self, account_type, account_no, first_name, last_name, pin, balance=0):
        self.account_type = account_type
        self.account_no = account_no
        self.account_name = f"{first_name} {last_name}"
        self.pin = pin
        self.balance = balance
        self.transactions = []

# Authenticate pin Function
    def authenticate(self, entered_pin):
        return entered_pin == self.pin

# Deposite Function
    def deposit(self, amount):
        self.balance += amount
        self.log_transaction('Deposit', amount)

# Withdrwa Function
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.log_transaction('Witdrawal', amount)
        else:
            print("Insufcient funds!")
            
            
# Function for Transfering money
    def transfer(self, target_account, amount):
        if amount <= self.balance:
            self.balance -= amount
            target_account.deposit(amount)
            self.log_transaction(f'Transfer to {target_account.account_no}', amount)
        else:
            print("Insuficient funds !")
            
# Function for log_transaction
    def log_transaction(self, transaction_type, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append({'Timestamp': timestamp, 'Type': transaction_type, 'Amount': amount})


# function for displaying balance
    def display_balance(self):
        print(f"Account Type: {self.account_type}")
        print(f"Account No: {self.account_no}")
        print(f"Account Name: {self.account_name}")
        print(f"Balance: ${self.balance:.2f}")

# Function to save to file
    def save_to_file(self):
        filename = f"{self.account_no}_transactions.json"
        with open(filename, 'w') as file:
            json.dump(self.transactions, file)

# Function to create customer
def create_customer():
    account_type = input("Enter account type (Savings or Current): ").capitalize()
    account_no = input("Enter account number: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    pin = getpass("Enter 4-digit PIN: ")

    # Check if the account already exists
    if os.path.exists(f"{account_no}_transactions.json"):
        print("Account already exists. Choose a different account number.")
        return None

    customer = Customer(account_type, account_no, first_name, last_name, pin)
    return customer

# Function To Authenticate Customer
def authenticate_customer(customers):
    account_no = input("Enter account number: ")
    pin = getpass("Enter 4-digit PIN: ")

    if account_no in customers and customers[account_no].authenticate(pin):
        return customers[account_no]
    else:
        print("Authentication failed. Please check your account number and PIN.")
        return None

#  The OPeration function
def main():
    customers = {}
    while True:
        print("\nMicro Bank Operations:")
        print("1. Create Account")
        print("2. Authenticate")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            customer = create_customer()
            if customer:
                customers[customer.account_no] = customer
                print("Account created successfully.")
        elif choice == '2':
            customer = authenticate_customer(customers)
            if customer:
                while True:
                    print("\nCustomer Operations:")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Transfer")
                    print("4. Display Balance")
                    print("5. Logout")

                    operation = input("Enter your operation (1/2/3/4/5): ")

                    if operation == '1':
                        amount = float(input("Enter deposit amount: "))
                        customer.deposit(amount)
                    elif operation == '2':
                        amount = float(input("Enter withdrawal amount: "))
                        customer.withdraw(amount)
                    elif operation == '3':
                        target_account_no = input("Enter target account number: ")
                        target_account = customers.get(target_account_no)
                        if target_account:
                            amount = float(input("Enter transfer amount: "))
                            customer.transfer(target_account, amount)
                        else:
                            print("Target account not found.")
                    elif operation == '4':
                        customer.display_balance()
                    elif operation == '5':
                        customer.save_to_file()
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid operation. Please try again.")
        elif choice == '3':
            print("Exiting Micro Bank. Have a great day!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
