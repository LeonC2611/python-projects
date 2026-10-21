from tabulate import tabulate
import csv
from cryptography import fernet
import sys
from pathlib import Path
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Global variables 
username = input('Enter username: ')
password = ""
fieldnames = ["Username", "Password", "Description"]
file = Path(f"{username}.csv")
ph = PasswordHasher()
# Login function
def login():
    while True:
        password = input("Enter password: ")
        with open(f"{username}.csv", newline="") as user_csv:
            reader = csv.DictReader(user_csv)
            user = list(filter(lambda u: username == u["Username"], reader))
            user = user[0]
            user_p = user["Password"]
            try:
                ph.verify(user_p, password)
                print("Correct!\n\n")
                break
            except VerifyMismatchError:
                print("Incorrect password try again")

                
# Prints the main menu
def main_menu():
    print("What would you like to do?")
    print("1. Show credentials list")
    print("2. Add new credentials")
    print("3. Change password")
    print("4. Delete credentials")
    print("5. Exit\n")
    while True:
        try:
            option = int(input("Please input the number corresponding your option: "))
            print("")
            if 0 >= option or option > 5:
                print("Please choose a number from 1-3\n")
            elif option == 5:
                sys.exit("Goodbye!")
            else:
                return option
        except ValueError:
            print("Not a number, please try again\n")
# Prints the main table
def show_table():
    with open(f"{username}.csv", "r", newline="") as user_csv:
        reader = csv.reader(user_csv)
        creds = list(reader)
        data = [cred for position, cred in enumerate(creds) if position != 0]
        headers = fieldnames
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print("")

# Adding credentials
def add_creds():
    with open(f"{username}.csv", "a", newline="") as user_csv:
        username_new = input("Please input username for new account: ")
        password = input("Please input password for new account: ")
        description = input("What are these credentials for: ")
        print("")
        u_name = [{"Username" : username_new, "Password" : password, "Description" : description}]
        writer = csv.DictWriter(user_csv, fieldnames=fieldnames)
        writer.writerows(u_name)
        print("Credentials have been added!\n")

# Change password function
def change_pswd():
    with open(f"{username}.csv", "r", newline="") as user_csv:
            reader = csv.reader(user_csv)
            creds = list(reader)
            data = [cred for position, cred in enumerate(creds) if position != 0]
            while True:
                account = input("Which account password do you want to replace? ")
                new_password = list(filter(lambda row: account == row[0], data))
                if new_password == []:
                    print("No account found, try again.\n")
                else:
                    account = new_password[0]
                    new_password = input("Please type in the new password: ")
                    print("")
                    account[1] = new_password
                    with open(f"{username}.csv", "w", newline="") as pwsd_csv:
                        writer = csv.writer(pwsd_csv)
                        writer.writerow(fieldnames)
                    with open(f"{username}.csv", "a", newline="") as pwsd_csv:
                        writer = csv.writer(pwsd_csv)
                        writer.writerows(data)
                    print("Password changed\n")
                    break
# Function to delete credentials
def dlt_creds():
    with open(f"{username}.csv", "r", newline="") as user_csv:
        reader = csv.reader(user_csv)
        data = list(reader)
        data = [cred for position, cred in enumerate(data) if position != 0]
        while True:
            account = input("Which account do you want to delete? ")
            all_accounts = list(filter(lambda row: account == row[0], data))
            dlt_account = list(filter(lambda row: account != row[0], data))
            if all_accounts == []:
                print("No account found, please try again.\n")
            else:
                with open(f"{username}.csv", "w", newline="") as dlt_acc:
                    writer = csv.writer(dlt_acc)
                    writer.writerow(fieldnames)
                with open(f"{username}.csv", "a", newline="") as dlt_acc:
                    writer = csv.writer(dlt_acc)
                    writer.writerows(dlt_account)
                print("Account deleted\n")
                break
# Main function that ties everything together
if file.exists():
    login()
    while True:
        menu = main_menu()
        if menu == 1:
            table = show_table()
        elif menu == 2:
            add_creds()
        elif menu == 3:
            change_pswd()
        elif menu == 4:
            dlt_creds()
# Creating account 
else:
    with open(f"{username}.csv", "w", newline="") as user_csv:
        writer = csv.DictWriter(user_csv, fieldnames=fieldnames)
        writer.writeheader()
    password = input("Please create a password: ")
    stored_pwsd = ph.hash(password)

    with open(f"{username}.csv", "a", newline="") as user_csv:
        u_name = [{"Username": username, "Password" : stored_pwsd, "Description" : "Password manager credentials"}]
        writer = csv.DictWriter(user_csv, fieldnames=fieldnames)
        writer.writerows(u_name)


