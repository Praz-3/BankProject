__author__ = 'user'

import database
from classes import Account,Savings,Current,Address
import database_admin as db_admin


def change_address(id):
    ch = 1
    addr = ""

    print("-- Menu --")
    print("1. Change Address Line 1")
    print("2. Change Address Line 2")
    print("3. Change State")
    print("4. Change City")
    print("5. Change Pincode")
    print("6. Quit")

    while ch != 6:

        try:
            ch = int(input())
        except:
            print("Invalid Choice")
            ch = 1
            continue

        if ch == 1:
            addr = input("Enter New Address Line 1\n")

        elif ch == 2:
            addr = input("Enter New Address Line 2\n")

        elif ch == 3:
            addr = input("Enter New State\n")

        elif ch == 4:
            addr = input("Enter New City\n")

        elif ch == 5:
            addr = input("Enter New Pincode\n")

        elif ch == 6:
            break

        database.change_address_customer(ch,id,addr)


def deposit_money(id):
    try:
        acc_no = int(input("Enter your account No\n"))
    except:
        print("Invalid Account No")
        return
    account = database.get_all_info_account(acc_no,id,"deposit")
    if account is not None:
        try:
            amount = int(input("Enter amount to Deposit\n"))
        except:
            print("Invalid Amount")
            return
        if account.deposit(amount):
            database.money_deposit_customer(account,amount)
            print("Rs ",amount,"Successfully deposited")
            print("Balance : Rs ",account.get_balance())

    else:
        print("Sorry Account No doesn't match")


def withdraw_money(id):
    try:
        acc_no = int(input("Enter your account No\n"))
    except:
        print("Invalid Account No")
        return
    account = database.get_all_info_account(acc_no,id,"withdraw")
    if account is not None:
        if account.get_withdrawals_left() == 0 and account.get_account_type() == "savings":
            print("Sorry You have exceeded withdrawals(10) for this month")

        else:
            try:
                amount = int(input("Enter amount to Withdraw\n"))
            except:
                print("Invalid Amount")
                return
            if account.withdraw(amount):
                database.money_withdraw_customer(account, amount,"withdraw")
                print("Rs ",amount,"Successfully withdrawn")
                print("Balance : Rs ", account.get_balance())

    else:
            print("Sorry Account No doesn't match")


def print_statement(id):
    try:
        acc_no = int(input("Enter your account No\n"))
    except:
        print("Invalid Account No")
        return
    account = database.get_all_info_account(acc_no,id,"statement")
    if account is not None:
        res = database.get_transactions_account(acc_no)
        print("Date \t\t\t Transaction Type \t\t\t Amount \t\t\t Balance \t")
        for i in range(0,len(res)):
            print(res[i][0].strftime("%Y-%b-%d")," \t\t\t ",res[i][1]," \t\t\t ",res[i][2]," \t\t\t ",res[i][3])
    else:
        print("No transactions!")


def transfer_money(id):
    try:
        acc_no_sender = int(input("Enter Account No From : "))
    except:
        print("Invalid Account No")
        return
    account_sender = database.get_all_info_account(acc_no_sender,id,"withdraw")
    if account_sender is not None:
        try:
            acc_no_receiver = int(input("Enter Account No To Transfer Money To : "))
        except:
            print("Invalid Account No")
            return
        account_receiver = database.get_all_info_account(acc_no_receiver,-1,"transfer")
        if account_receiver is not None:
            try:
                amount = int(input("\nEnter Amount To Transfer : "))
            except:
                print("Invalid Amount")
                return
            database.transfer_money_customer(account_sender,account_receiver,amount)
        else:
            print("Sorry Account doesn't exist")

    else:
        print("Sorry Account No doesn't match")


def close_account(id):
    try:
        acc_no = int(input("\nEnter Account No to close : "))
    except:
        print("Invalid Account No")
        return
    account = database.get_all_info_account(acc_no,id,"close")
    if account is not None:
        database.close_account_customer(account)
    else:
        print("\nSorry Account No doesn't match")

