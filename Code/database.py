from dbConnection import con, cur
from classes import Customer,Account,Savings,Current
import datetime


def sign_up_customer(customer):
    fname = customer.get_first_name()
    lname = customer.get_last_name()
    password = customer.get_password()
    sql = "select customer_id from customers order by customer_id desc limit 1"
    cur.execute(sql)
    res = cur.fetchall()
    c_id = int(res[0][0])+1
    status = customer.get_status()
    att = customer.get_login_attempts()
    sql = "insert into customers values(%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, (int(c_id), fname, lname,  status, int(att),password))
    line1 = customer.get_addr_line1()
    line2 = customer.get_addr_line2()
    city = customer.get_addr_city()
    state = customer.get_addr_state()
    pincode = int(customer.get_addr_pincode())
    sql = "insert into address values(%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, (c_id,line1,line2,city,state,pincode))
    con.commit()
    print("Congratulations ! Your Account was Created Successfully")
    print("Your Customer ID : ",c_id)
    return c_id


def open_acc(c_id, account):
    acc_type = account.get_account_type()
    bal = account.get_balance()
    withdrawals_left = account.get_withdrawals_left()
    sql = "select account_no from accounts order by account_no desc limit 1"
    cur.execute(sql)
    res = cur.fetchall()
    acc_no = int(res[0][0])+1
    account.set_account_no(acc_no)
    account.open_account(bal)
    status = "open"
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    sql = "insert into accounts values (%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(sql, (c_id, acc_no, date, acc_type, status, int(bal), withdrawals_left))
    con.commit()
    print("Account Opened Successfully")
    print("Account No is : ", acc_no)


def get_all_info_customer(id):
    sql = "select * from customers where customer_id = %s"
    cur.execute(sql, (id))
    res = cur.fetchall()
    if len(res) == 0:
        return None
    customer = Customer()
    status = res[0][3]
    att = res[0][4]
    customer.set_customer_id(id)
    customer.set_status(status)
    customer.set_login_attempts(att)
    return customer


def login_customer(id, password):
    sql = "select count(*) from customers where customer_id = %s and password = %s"
    cur.execute(sql, (id, password))
    res = cur.fetchall()
    count = res[0][0]
    if count == 1:
        return True
    else:
        return False


def reset_login_attempts(id):
    sql = "update customers set login_attempts = 3 where customer_id = %s"
    cur.execute(sql, (id))
    con.commit()


def update_customer(customer):
    id = customer.get_customer_id()
    status = customer.get_status()
    att = customer.get_login_attempts()
    sql = "update customers set status = %s,login_attempts = %s where customer_id = %s"
    cur.execute(sql, (status, att, id))
    con.commit()


def change_address_customer(ch, id, addr):
    if ch == 1:
        sql = "update address set line1 = %s where customer_id = %s"
        cur.execute(sql, (addr, id))

    elif ch == 2:
        sql = "update address set line2 = %s where customer_id = %s"
        cur.execute(sql, (addr, id))

    elif ch == 3:
        sql = "update address set state = %s where customer_id = %s"
        cur.execute(sql, (addr, id))

    elif ch == 4:
        sql = "update address set city = %s where customer_id = %s"
        cur.execute(sql, (addr, id))

    elif ch == 5:
        sql = "update address set pincode = %s where customer_id = %s"
        cur.execute(sql, (addr, id))

    else:
        return

    con.commit()
    print("Details Updated Successfully")


def get_all_info_account(acc_no, id, msg):
    account = None
    sql = None
    if msg == "transfer":
        sql = "select * from accounts where account_no = %s and account_type != 'fd' and status = 'open'"
        cur.execute(sql, (acc_no))
    else:
        sql = "select * from accounts where account_no = %s and customer_id = %s and status = 'open'"
        cur.execute(sql, (acc_no, id))

    res = cur.fetchall()
    if len(res) == 0:
        return None

    account_no = res[0][1]
    account_type = res[0][3]
    balance = res[0][5]
    wd_left = res[0][6]
    if account_type == "savings":
        account = Savings()
    else:
        account = Current()

    account.set_account_type(account_type)
    account.set_balance(balance)
    account.set_account_no(account_no)
    account.set_withdrawals_left(wd_left)
    return account


def money_deposit_customer(account, amount):
    bal = account.get_balance()
    acc_no = account.get_account_no()
    type = "credit"
    sql = "update accounts set balance = %s where account_no = %s"
    cur.execute(sql, (bal, acc_no))
    sql = "select transaction_id from transactions order by transaction_id desc limit 1"
    cur.execute(sql)
    res = cur.fetchall()
    t_id = int(res[0][0]) + 1
    sql = "insert into transactions values (%s,%s,%s,%s,%s,%s)"
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    cur.execute(sql, (t_id, acc_no, type, amount, bal, date))
    con.commit()


def money_withdraw_customer(account, amount, msg):
    acc_type = account.get_account_type()
    wd_left = account.get_withdrawals_left()
    bal = account.get_balance()
    acc_no = account.get_account_no()
    type = "debit"
    sql = "update accounts set balance = %s where account_no = %s"
    cur.execute(sql, (bal, acc_no))
    sql = "select transaction_id from transactions order by transaction_id desc limit 1"
    cur.execute(sql)
    res = cur.fetchall()
    t_id = int(res[0][0]) + 1
    sql = "insert into transactions values (%s,%s,%s,%s,%s,%s)"
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    cur.execute(sql, (t_id, acc_no, type, amount, bal, date))
    if acc_type == "savings" and msg != "transfer":
        wd_left -= 1
        sql = "update accounts set withdrawals_left = %s where account_no = %s"
        cur.execute(sql, (wd_left, acc_no))
    con.commit()


def get_transactions_account(acc_no):
    sql = "select transaction_date,type,amount,balance from transactions where account_no = %s order by transaction_id"
    cur.execute(sql, (acc_no))
    res = cur.fetchall()
    return res


def transfer_money_customer(account_sender,account_receiver,amount):
    if account_sender.withdraw(amount):
        account_receiver.deposit(amount)
        money_withdraw_customer(account_sender,amount,"transfer")
        money_deposit_customer(account_receiver,amount)
        print("Transfer Completed !")
        print("New Balance for Account No ",account_sender.get_account_no()," : ",account_sender.get_balance())
        print("New Balance for Account No ",account_receiver.get_account_no()," : ",account_receiver.get_balance())


def close_account_customer(account):
    acc_no = account.get_account_no()
    balance = account.get_balance()
    sql = "update accounts set status='closed',balance = 0 where account_no = %s"
    cur.execute(sql, (acc_no))
    closed_on = datetime.datetime.now().strftime("%Y-%m-%d")
    sql = "insert into closed_accounts values(%s,%s)"
    cur.execute(sql, (acc_no, closed_on))
    print("Account Closed Successfully !")
    print("Rs ",balance," will be delivered to your address shortly")
    con.commit()
