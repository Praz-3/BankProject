from classes import Customer,Account,Savings,Current,Address
import database, database_admin, login_menu, admin_menu


def signUp():

    customer = Customer()
    first_name = input("Enter First Name\n")
    last_name = input("Enter Last Name\n")
    add_line1 = input("Enter Address Line 1\n")
    add_line2 = input("Enter Address Line 2\n")
    city = input("Enter City\n")
    state = input("Enter State\n")
    pincode = int(input("Enter Pincode\n"))
    password = input("Enter password (min 8 char and max 20 char)\n")
    while len(password) < 8 or len(password) > 20:
        print("Please Enter password in given range\n")
        password = input()

    t = input("Select acc type(Enter 1/2):\n\t1.Savings\n\t2.Current\n")
    msg = "Enter amount "
    withdrawals_left = 200
    account = None

    if t == '1':
        account = Savings()
        acc_type = "savings"
        msg += "(min 5000): "
        withdrawals_left = 10
    else:
        account = Current()
        acc_type = "current"
        msg += ": "
    bal = int(input(msg))

    customer.set_first_name(first_name)
    customer.set_last_name(last_name)
    customer.set_password(password)
    customer.set_status("open")
    customer.set_login_attempts(3)

    addr = Address()
    addr.set_line_1(add_line1)
    addr.set_line_2(add_line2)
    addr.set_city(city)
    addr.set_state(state)
    addr.set_pincode(pincode)

    customer.set_address(addr)
    account.set_account_type(acc_type)
    account.set_balance(bal)
    account.set_withdrawals_left(withdrawals_left)

    c_id = database.sign_up_customer(customer)
    database.open_acc(c_id, account)


def signIn():

    id = int(input("Enter Customer ID\n"))
    if database_admin.check_customer_exists(id):
        customer = database.get_all_info_customer(id)
        if customer.get_status() == "locked":
            print("Sorry your account has been bloacked due to 3 unsuccessful attempts")
            return
        password = input("Enter password:\n")
        res = database.login_customer(id,password)
        if res is True:
            database.reset_login_attempts(id)
            print("Login Successful")
            ch = 1
            while ch != 0:
                print("\n--- Menu ---")
                print("1. Address Change")
                print("2. Money Deposit")
                print("3. Money Withdrawal")
                print("4. Print Statement")
                print("5. Transfer Money")
                print("6. Account Closure")
                print("0. Customer Logout")

                try:
                    ch = int(input())
                except:
                    print("Invalid Choice")
                    ch = 1
                    continue

                if ch == 1:
                    login_menu.change_address(id)
                elif ch == 2:
                    login_menu.deposit_money(id)
                elif ch == 3:
                    login_menu.withdraw_money(id)
                elif ch == 4:
                    login_menu.print_statement(id)
                elif ch == 5:
                    login_menu.transfer_money(id)
                elif ch == 6:
                    login_menu.close_account(id)
                elif ch == 0:
                    print("Logged Out Successfully")
                else:
                    print("Invalid Choice")
        else:
            att = customer.get_login_attempts() - 1
            customer.set_login_attempts(att)
            database.update_customer(customer)
            print("Incorrect Password")

    else:
        print("Customer doesn't exist")


def adminSignIn():
    try:
        id = input("\nEnter Admin ID : ")
    except:
        print("Invalid ID")
        return

    password = input("\nEnter Password : ")
    count = 2
    if id == "admin" and password == "Pass1234":
        res = True
    else:
        res = False

    while count != 0 and res == False:
        print("Wrong ID or Password")
        print("Attempts Remaining : ", count)
        try:
            id = int(input("Enter Admin ID\n"))
        except:
            print("Invalid ID")
            return
        password = input("Enter Password\n")
        if id == "admin" and password == "Pass1234":
            res = True
        else:
            res = False
        count = count - 1
    if res:
        print("Login Successful")
        ch = 1
        while ch != 0:
            print("\n --- Menu --- ")
            print("1. Print Closed Accounts History")
            print("0. Admin Log Out")

            try:
                ch = int(input())
            except:
                print("Invalid Choice")
                ch = 1
                continue
            if ch == 1:
                admin_menu.print_closed_acc_history()
            elif ch == 0:
                print("Logged Out Successfully")
            else:
                print("Invalid Choice")

    else:
        print("Sorry all Attempts Finished")
