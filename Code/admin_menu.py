import database_admin as db_admin


def print_closed_acc_history():
    res = db_admin.get_closed_accounts()
    print("Account No \t\t\t Closed On")
    for i in range(0, len(res)):
        print(res[i][0], " \t\t\t\t ", res[i][1].strftime("%Y-%b-%d"))
