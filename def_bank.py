# USING FUNCTION 

#This program allows users to create accounts, authenticate, and perform banking operations. 
#It saves transactions to a JSON file for each customer.


import json
import os
from getpass import getpass
from datetime import datetime


def create_customer(customers):
    """
    Function to create a new customer account.
    """
    account_type = input("Enter account type (Savings or Current): ").capitalize()
    account_no = input("Enter account number: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    pin = getpass("Enter 4-digit PIN: ")

    # Check if the account already exists
    if account_no in customers:
        print("Account already exists. Choose a different account number.")
        return None
  
    customer = {
        'AccountType': account_type,
        'AccountNo': account_no,
        'AccountName': f"{first_name} {last_name}",
        'PIN': pin,
        'Balance': 0,
        'Transactions': []
    }

    customers[account_no] = customer
    return customer

def authenticate_customer(customers):
    """
    Function to authenticate a customer.
    """
    account_no = input("Enter account number: ")
    pin = getpass("Enter 4-digit PIN: ")

    if account_no in customers and customers[account_no]['PIN'] == pin:
        return customers[account_no]
    else:
        print("Authentication failed. Please check your account number and PIN.")
        return None

def deposit(customer, amount):
    """
    Function to deposit money into an account.
    """
    customer['Balance'] += amount
    log_transaction(customer, 'Deposit', amount)

def withdraw(customer, amount):
    """
    Function to withdraw money from an account.
    """
    if amount <= customer['Balance']:
        customer['Balance'] -= amount
        log_transaction(customer, 'Withdrawal', amount)
    else:
        print("Insufficient funds!")

def transfer(sender, recipient, amount):
    """
    Function to transfer money between two accounts.
    """
    if amount <= sender['Balance']:
        sender['Balance'] -= amount
        recipient['Balance'] += amount
        log_transaction(sender, f'Transfer to {recipient["AccountNo"]}', amount)
    else:
        print("Insufficient funds!")

def log_transaction(customer, transaction_type, amount):
    """
    Function to log a transaction.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaction = {'Timestamp': timestamp, 'Type': transaction_type, 'Amount': amount}
    customer['Transactions'].append(transaction)

def display_balance(customer):
    """
    Function to display the account balance.
    """
    print(f"Account Type: {customer['AccountType']}")
    print(f"Account No: {customer['AccountNo']}")
    print(f"Account Name: {customer['AccountName']}")
    print(f"Balance: ${customer['Balance']:.2f}")

def save_to_file(customer):
    """
    Function to save customer transactions to a file.
    """
    filename = f"{customer['AccountNo']}_transactions.json"
    with open(filename, 'w') as file:
        json.dump(customer['Transactions'], file)

def main():
    """
    Main function to run the micro bank simulation.
    """
    customers = {}
    while True:
        print("\nMicro Bank Operations:")
        print("1. Create Account")
        print("2. Authenticate")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            customer = create_customer(customers)
            if customer:
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
                        deposit(customer, amount)
                    elif operation == '2':
                        amount = float(input("Enter withdrawal amount: "))
                        withdraw(customer, amount)
                    elif operation == '3':
                        target_account_no = input("Enter target account number: ")
                        target_account = customers.get(target_account_no)
                        if target_account:
                            amount = float(input("Enter transfer amount: "))
                            transfer(customer, target_account, amount)
                        else:
                            print("Target account not found.")
                    elif operation == '4':
                        display_balance(customer)
                    elif operation == '5':
                        save_to_file(customer)
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
