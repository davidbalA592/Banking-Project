import cx_Oracle
import re
from datetime import datetime
con = cx_Oracle.connect("DAVIDBALA/rec@XE")
cur = con.cursor()


class Customer():
    def set_first_name(self,fname):
        self.first_name = fname

    def set_last_name(self,lname):
        self.last_name = lname

    def set_customer_id(self,id):
        self.customer_id = id;

    def set_password(self,pwd):
        self.password = pwd

    def set_login_attempts(self,att):
        self.login_attempts = att
        if att == 0:
            self.status = "locked"

    def set_status(self,status):
        self.status = status

    def set_address(self,addr):
        self.addr = addr

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_customer_id(self):
        return self.customer_id

    def get_password(self):
        return self.password

    def get_login_attempts(self):
        return self.login_attempts

    def get_status(self):
        return self.status

    def get_addr_line1(self):
        return self.addr.line1

    def get_addr_city(self):
        return self.addr.city

    def get_addr_state(self):
        return self.addr.state

    def get_addr_pincode(self):
        return self.addr.pincode


class Account():

    def set_account_no(self,acc_no):
        self.account_no = acc_no

    def set_account_type(self,type):
        self.type = type

    def set_balance(self,bal):
        self.balance = bal

    def set_withdrawals_left(self,wd):
        self.withdrawals_left = wd

    def get_account_no(self):
        return self.account_no

    def get_balance(self):
        return self.balance

    def get_account_type(self):
        return self.type

    def get_withdrawals_left(self):
        return self.withdrawals_left



class Savings(Account):

    interest = 7.5;
    min_balance = 0;

    def open_account(self,amount):
        if amount < 0:
            print("Please input a valid amount")
            return False
        else:
            self.balance = amount
            return True

    def deposit(self,amount):
        if amount < 0:
            print("Please input a valid amount");
            return False
        else:
            self.balance += amount;
            return True


    def withdraw(self,amount):
        if amount > self.balance:
            print("Sorry You don't have enough balance");
            return False
        else:
            self.balance -= amount;
            return True

class Current(Account):

    interest = 0
    min_balance = 5000

    def open_account(self,amount):
        if amount < self.min_balance:
            print("Please input a valid amount")
            return False
        else:
            self.balance = amount
            return True

    def deposit(self,amount):
        if amount < 0:
            print("Please input a valid amount");
            return False
        else:
            self.balance += amount;
            return True


    def withdraw(self,amount):
        if amount > self.balance:
            print("Sorry You don't have enough balance");
            return False
        elif self.balance - amount < 5000:
            print("Sorry You can't withdraw this much money as you need at least Rs",self.min_balance," to maintain this account")
            return False
        else:
            self.balance -= amount;
            return True


class Address():

    def set_line_1(self,line1):
        self.line1 = line1

    def set_city(self,city):
        self.city = city

    def set_state(self,state):
        self.state = state

    def set_pincode(self,pincode):
        self.pincode = pincode

        
def sign_up():

    customer = Customer()
    first_name = input("Enter First Name\n")
    last_name = input("Enter Last Name\n")
    add_line1 = input("Enter Address \n")
    city = input("Enter City\n")
    state = input("Enter State\n")
    try:
        pincode = int(input("Enter Pincode\n"))
        if pincode < 100000 or pincode > 999999:
            print("Invalid Pincode")
            return
    except:
        print("Invalid Pincode")
        return

    password = input("Enter password (min 8 char and max 20 char)\n")
    while len(password) < 8 or len(password) > 20:
        print("Please Enter password in given range\n")
        password = input();

    customer.set_first_name(first_name)
    customer.set_last_name(last_name)
    customer.set_password(password)
    customer.set_status("open")
    customer.set_login_attempts(3)

    addr = Address()
    addr.set_line_1(add_line1)
    addr.set_city(city)
    addr.set_state(state)
    addr.set_pincode(pincode)

    customer.set_address(addr)

    sign_up_customer(customer)

def sign_in():
    try:
        id = int(input("Enter Customer ID\n"))
    except:
        print("Invalid ID")
        return

    if check_customer_exists(id) is True:
        customer = get_all_info_customer(id)
        if customer.get_status() == "locked":
            print("Sorry Your Account has been locked due to 3 unsuccessful login attempts")
            return
        password = input("Enter Password\n")
        res = login_customer(id,password)
        if res is True:
            reset_login_attempts(id)
            print("Login Successful")
            ch = 1
            while ch != 0:
                print("\n--- Menu ---")
                print("1. Address Change")
                print("2. Open New Account")
                print("3. Money Deposit")
                print("4. Money Withdrawal")
                print("5. Transfer Money")
                print("6. Print Statement")
                print("7. Account Closure")
                print("8. Add Credit Card")
                print("0. Logout")

                try:
                    ch = int(input())
                except:
                    print("Invalid Choice")
                    ch = 1
                    continue

                if ch == 1:
                    change_address(id)
                elif ch == 2:
                    open_new_account(id)
                elif ch == 3:
                    deposit_money(id)
                elif ch == 4:
                    withdraw_money(id)
                elif ch == 5:
                    transfer_money(id)
                elif ch == 6:
                    print_statement(id)
                elif ch == 7:
                    close_account(id)
                elif ch == 8:
                    add_credit_card(id)
                elif ch == 0:
                    print("Logged Out Successfully")
                else:
                    print("Invalid Choice")

        else:
            att = customer.get_login_attempts()-1
            customer.set_login_attempts(att)
            update_customer(customer)
            print("Incorrect Password")


    else:
        print("Customer doesn't exist")


def get_closed_accounts():
    sql = "select * from closed_accounts"
    cur.execute(sql)
    res = cur.fetchall()
    return res

def print_closed_acc_history():
    res = get_closed_accounts()
    print("Account No \t\t\t Closed On")
    for i in range(0,len(res)):
        print(res[i][0]," \t\t\t\t ",res[i][1].strftime("%d-%b-%Y"))

def login_admin(id,password):
    sql = "select count(*) from admin where admin_id = :id and password = :password"
    cur.execute(sql , {"id":id, "password":password})
    res = cur.fetchall()
    count = res[0][0]
    if count == 1:
        return True
    else:
        return False

    
def admin_sign_in():
    try:
        id = input("\nEnter Admin ID : ")
    except:
        print("Invalid ID")
        return

    password = input("\nEnter Password : ")
    count = 2
    res = login_admin(id,password)

    while count != 0 and res == False:
        print("Wrong ID or Password")
        print("Attempts Remaining : ",count)
        try:
            id = int(input("Enter Admin ID\n"))
        except:
            print("Invalid ID")
            return
        password = input("Enter Password\n")
        res = login_admin(id,password)
        count = count-1

    if res == True:
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
                print_closed_acc_history()
            elif ch == 0:
                print("Logged Out Successfully")
            else:
                print("Invalid Choice")

    else:
        print("Sorry all Attempts Finished")

def make_all_tables():
    sql = "select count(*) from user_tables where table_name = 'CUSTOMERS'"
    cur.execute(sql)
    res = cur.fetchall()
    if res[0][0] != 0:
        return


    sql = """create table customers(
                  customer_id number(5) primary key,
                  first_name varchar2(10),
                  last_name varchar2(10),
                  status varchar2(10),
                  login_attempts number(3),
                  password varchar2(20))"""
    cur.execute(sql)

    sql = """create table address(
                  customer_id number(5),
                  line1 varchar2(30),
                  city varchar2(30),
                  state varchar2(30),
                  pincode number(6),
                  constraint fk_addr foreign key(customer_id) references customers(customer_id))"""
    cur.execute(sql)

    sql = """create table accounts(
                  customer_id number(5),
                  account_no number(5) primary key,
                  opened_on date,
                  account_type varchar2(10),
                  status varchar2(10),
                  balance number(8),
                  withdrawals_left number(3),
                  next_reset_date date,
                  constraint fk_acc foreign key(customer_id) references customers(customer_id))"""
    cur.execute(sql)

    sql = """create table transactions(
                  transaction_id number(5) primary key,
                  account_no number(5),
                  type varchar2(10),
                  amount number(8),
                  balance number(8),
                  transaction_date date,
                  constraint fk_transaction_account_no foreign key(account_no) references accounts(account_no))"""
    cur.execute(sql)

    sql = """create table admin(
                  admin_id number(5),
                  password varchar2(10))"""
    cur.execute(sql)

    sql = """create table closed_accounts(
                  account_no number(5),
                  closed_on date,
                  constraint fk_closed_acc foreign key(account_no) references accounts(account_no))"""
    cur.execute(sql)

    sql = """create table credit_card(
                  cc_no number(5) primary key,
                  account_no number(5),
                  amount number(8),
                  constraint fk_credit_card foreign key(account_no) references accounts(account_no))"""
    cur.execute(sql)


    sql = """create sequence customer_id_sequence
            start with 1
            increment by 1
            nocycle"""
    cur.execute(sql)

    sql = """create sequence cc_no_sequence
            start with 3388000
            increment by 1
            nocycle"""
    cur.execute(sql)

    sql = """create sequence account_no_sequence
            start with 1
            increment by 1
            nocycle"""
    cur.execute(sql)

    sql = """create sequence transaction_id_sequence
            start with 1
            increment by 1
            nocycle"""
    cur.execute(sql)

    sql = "insert into admin values(3,'davidbala')"
    cur.execute(sql)

    con.commit()

def reset_withdrawals():
    sql = """update accounts set withdrawals_left = 10,next_reset_date = add_months(next_reset_date,1)
              where account_type = 'savings' and sysdate >= next_reset_date"""
    cur.execute(sql)
    con.commit()
    

        
#working with database
    
def sign_up_customer(customer):
    fname = customer.get_first_name()
    lname = customer.get_last_name()
    password = customer.get_password()
    sql = "select customer_id_sequence.nextval from dual"
    cur.execute(sql)
    res = cur.fetchall()
    id = res[0][0]
    status = customer.get_status()
    att = customer.get_login_attempts()
    sql = "insert into customers values(:id,:fname,:lname,:status,:att,:password)"
    cur.execute(sql, {"id":id, "fname":fname, "lname":lname , "password":password, "status":status, "att":att})
    line1 = customer.get_addr_line1()
    city = customer.get_addr_city()
    state = customer.get_addr_state()
    pincode = customer.get_addr_pincode()
    sql = "insert into address values(:id,:line1,:city,:state,:pincode)"
    cur.execute(sql, {"id":id, "line1":line1, "city":city, "state":state, "pincode":pincode} )
    con.commit()
    print("Congratulations ! Your Account was Created Successfully")
    print("Your Customer ID : ",id)

def login_customer(id,password):
    sql = "select count(*) from customers where customer_id = :id and password = :password"
    cur.execute(sql, {"id":id, "password":password})
    res = cur.fetchall()
    count = res[0][0]
    if count == 1:
        return True
    else:
        return False

def open_new_account_customer(account,cus_id):
    withdrawals_left = None
    account_type = account.get_account_type()
    bal = account.get_balance()
    opened_on = datetime.now().strftime("%d-%b-%Y")
    status = "open"
    sql = "select account_no_sequence.nextval from dual"
    cur.execute(sql)
    res = cur.fetchall()
    acc_no = res[0][0]
    if account_type == "savings":
        withdrawals_left = 10
    sql = "select add_months(sysdate,1) from dual"
    cur.execute(sql)
    res = cur.fetchall()
    next_date = res[0][0].strftime("%d-%b-%Y")
    sql = "insert into accounts values(:cus_id,:acc_no,:opened_on,:acc_type,:status,:bal,:wd,:next_date)"
    cur.execute(sql , {"cus_id":cus_id, "acc_no":acc_no, "opened_on":opened_on, "acc_type":account_type, "status":status, "bal":bal, "wd":withdrawals_left, "next_date":next_date})
    con.commit()
    print("Account Opened Successfully")
    print("Account No is : ",acc_no)

def change_address_customer(ch,id,addr):
    if ch == 1:
        sql = "update address set line1 = :line1 where customer_id = :id"
        cur.execute(sql, {"line1":addr, "id":id})

    elif ch == 2:
        sql = "update address set state = :state where customer_id = :id"
        cur.execute(sql, {"state":addr, "id":id})

    elif ch == 3:
        sql = "update address set city = :city where customer_id = :id"
        cur.execute(sql, {"city":addr, "id":id})

    elif ch == 4:
        sql = "update address set pincode = :pincode where customer_id = :id"
        cur.execute(sql, {"pincode":addr, "id":id})

    else:
        return

    con.commit()
    print("Details Updated Successfully")

def get_all_info_customer(id):
    sql = "select * from customers where customer_id = :id"
    cur.execute(sql, {"id":id})
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

def get_all_info_account(acc_no,id,msg):
    account = None
    sql = None
    if msg == "transfer":
        sql = "select * from accounts where account_no = :acc_no and account_type != 'fd' and status = 'open'"
        cur.execute(sql, {"acc_no":acc_no})
    else:
        sql = "select * from accounts where account_no = :acc_no and customer_id = :id and account_type != 'fd' and status = 'open'"
        cur.execute(sql, {"acc_no":acc_no, "id":id})

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


def money_deposit_customer(account,amount):
    bal = account.get_balance()
    acc_no = account.get_account_no()
    type = "credit"
    sql = "update accounts set balance = :bal where account_no = :acc_no"
    cur.execute(sql , {"bal":bal, "acc_no":acc_no})
    sql = "select transaction_id_sequence.nextval from dual"
    cur.execute(sql)
    res = cur.fetchall()
    t_id = res[0][0]
    sql = "insert into transactions values (:t_id,:acc_no,:type,:amount,:bal,:date_on)"
    date = datetime.now().strftime("%d-%b-%Y")
    cur.execute(sql , {"t_id":t_id, "acc_no":acc_no, "type":type , "amount":amount , "bal":bal, "date_on":date})
    con.commit()

def money_withdraw_customer(account,amount,msg):
    acc_type = account.get_account_type()
    wd_left = account.get_withdrawals_left()
    bal = account.get_balance()
    acc_no = account.get_account_no()
    type = "debit"
    sql = "update accounts set balance = :bal where account_no = :acc_no"
    cur.execute(sql , {"bal":bal, "acc_no":acc_no})
    sql = "select transaction_id_sequence.nextval from dual"
    cur.execute(sql)
    res = cur.fetchall()
    t_id = res[0][0]
    sql = "insert into transactions values (:t_id,:acc_no,:type,:amount,:bal,:date_on)"
    date = datetime.now().strftime("%d-%b-%Y")
    cur.execute(sql , {"t_id":t_id ,"acc_no":acc_no, "type":type , "amount":amount , "bal":bal, "date_on":date })
    if acc_type == "savings" and msg != "transfer":
        wd_left -= 1
        sql = "update accounts set withdrawals_left = :wd_left where account_no = :acc_no"
        cur.execute(sql, {"wd_left":wd_left, "acc_no":acc_no})
    con.commit()

def get_transactions_account(acc_no,date_from,date_to):
    sql = """select transaction_date,type,amount,balance from transactions where account_no = :acc_no
              and transaction_date between :date_from and :date_to order by transaction_id"""
    cur.execute(sql, {"acc_no":acc_no, "date_from":date_from, "date_to":date_to})
    res = cur.fetchall()
    return res

def transfer_money_customer(account_sender,account_receiver,amount):
    if account_sender.withdraw(amount) == True:
        account_receiver.deposit(amount)
        money_withdraw_customer(account_sender,amount,"transfer")
        money_deposit_customer(account_receiver,amount)
        print("Transfer Completed !")
        print("New Balance for Account No ",account_sender.get_account_no()," : ",account_sender.get_balance())
        print("New Balance for Account No ",account_receiver.get_account_no()," : ",account_receiver.get_balance())


def close_account_customer(account):
    acc_no = account.get_account_no()
    balance = account.get_balance()
    sql = "update accounts set status='closed',balance = 0 where account_no = :acc_no"
    cur.execute(sql, {"acc_no":acc_no})
    closed_on = datetime.now().strftime("%d-%b-%Y")
    sql = "insert into closed_accounts values(:acc_no,:closed_on)"
    cur.execute(sql, {"acc_no":acc_no, "closed_on":closed_on})
    print("Account Closed Successfully !")
    print("Rs ",balance," will be delivered to your address shortly")
    con.commit()

def reset_login_attempts(id):
    sql = "update customers set login_attempts = 3 where customer_id = :id"
    cur.execute(sql,{"id":id})
    con.commit()

def update_customer(customer):
    id = customer.get_customer_id()
    status = customer.get_status()
    att = customer.get_login_attempts()
    sql = "update customers set status = :status,login_attempts = :att where customer_id = :id"
    cur.execute(sql, {"status":status, "att":att, "id":id})
    con.commit()




def addcredit_card(account,amount):
    acc_no = account.get_account_no()
    sql = "select cc_no_sequence.nextval from dual"
    cur.execute(sql)
    res = cur.fetchall()
    c_no = res[0][0]
    sql = "insert into credit_card values (:c_no,:acc_no,:amount)"
    con.commit()


#admin Login
    
def check_customer_exists(id):
    sql = "select count(*) from customers where customer_id = :id"
    cur.execute(sql, {"id":id})
    res = cur.fetchall()
    count = res[0][0]
    if count == 1:
        return True
    else:
        return False

#transactions

def change_address(id):
    ch = 1
    addr = ""

    print("-- Menu --")
    print("1. Change Address Line 1")
    print("2. Change State")
    print("3. Change City")
    print("4. Change Pincode")
    print("5. Quit")

    while ch != 5:

        try:
            ch = int(input())
        except:
            print("Invalid Choice")
            ch = 1
            continue

        if ch == 1:
            addr = input("Enter New Address Line 1\n")

        elif ch == 2:
            addr = input("Enter New State\n")

        elif ch == 3:
            addr = input("Enter New City\n")

        elif ch == 4:
            addr = input("Enter New Pincode\n")

        elif ch == 5:
            break

        change_address_customer(ch,id,addr)

def get_new_account(ch,id):
    account = None
    acc_type = None
    msg = "Enter Balance "
    term = None
    if ch == 1:
        account = Savings()
        acc_type = "savings"
        msg += ": "
    elif ch == 2:
        account = Current()
        acc_type = "current"
        msg += "(min 5000) : "
    else:
        return None

    balance = int(input(msg))
    while account.open_account(balance) == False:
        balance = int(input("\nEnter Valid Balance : "))
    account.set_account_type(acc_type)
    return account
    
def open_new_account(id):
    account = None
    print("\n --- Menu --- ")
    print("1. Open Savings Account")
    print("2. Open Current Account")

    try:
        ch = int(input())
    except:
        print("Invalid Choice")
        return

    account = get_new_account(ch,id)
    if account is not None:
        open_new_account_customer(account,id)
    else:
        print("Invalid Choice")


def deposit_money(id):
    try:
        acc_no = int(input("Enter your account No\n"))
    except:
        print("Invalid Account No")
        return
    account = get_all_info_account(acc_no,id,"deposit")
    if account is not None:
        try:
            amount = int(input("Enter amount to Deposit\n"))
        except:
            print("Invalid Amount")
            return
        if account.deposit(amount) == True:
            money_deposit_customer(account,amount)
            print("Rs ",amount,"Successfully deposited");
            print("Balance : Rs ",account.get_balance())

    else:
        print("Sorry Account No doesn't match")

def withdraw_money(id):
    try:
        acc_no = int(input("Enter your account No\n"))
    except:
        print("Invalid Account No")
        return
    account = get_all_info_account(acc_no,id,"withdraw")
    if account is not None:
        if account.get_withdrawals_left() == 0 and account.get_account_type() == "savings":
            print("Sorry You have exceeded withdrawals(10) for this month")

        else:
            try:
                amount = int(input("Enter amount to Withdraw\n"))
            except:
                print("Invalid Amount")
                return
            if account.withdraw(amount) == True:
                money_withdraw_customer(account,amount,"withdraw")
                print("Rs ",amount,"Successfully withdrawn");
                print("Balance : Rs ",account.get_balance())

    else:
            print("Sorry Account No doesn't match")

def print_statement(id):
    try:
        acc_no = int(input("Enter your account No\n"))
    except:
        print("Invalid Account No")
        return
    account = get_all_info_account(acc_no,id,"statement")
    if account is not None:
        print("Enter Dates in format (day-Mon-Year) ")
        date_from = input("Date From : ")
        date_to = input("\nDate To : ")
        if validate_date(date_from,date_to) == True:
            res = get_transactions_account(acc_no,date_from,date_to)
            print("Date \t\t\t Transaction Type \t\t\t Amount \t\t\t Balance \t")
            for i in range(0,len(res)):
                print(res[i][0].strftime("%d-%b-%Y")," \t\t\t ",res[i][1]," \t\t\t ",res[i][2]," \t\t\t ",res[i][3])
        else:
            print("Please Enter Valid Dates")

def transfer_money(id):
    try:
        acc_no_sender = int(input("Enter Account No From : "))
    except:
        print("Invalid Account No")
        return
    account_sender = get_all_info_account(acc_no_sender,id,"withdraw")
    if account_sender is not None:
        try:
            acc_no_receiver = int(input("Enter Account No To Transfer Money To : "))
        except:
            print("Invalid Account No")
            return
        account_receiver = get_all_info_account(acc_no_receiver,-1,"transfer")
        if account_receiver is not None:
            try:
                amount = int(input("\nEnter Amount To Transfer : "))
            except:
                print("Invalid Amount")
                return
            transfer_money_customer(account_sender,account_receiver,amount)
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
    account = get_all_info_account(acc_no,id,"close")
    if account is not None:
        close_account_customer(account)
    else:
        print("\nSorry Account No doesn't match")


def add_credit_card(id):
    try:
        acc_no = int(input("Enter your account No\n"))
    except:
        print("Invalid Account No")
        return
    account = get_all_info_account(acc_no,id,"deposit")
    if account is not None:
        try:
            amount = int(input("Enter the amount(must be greater then 30,000)\n"))
        except:
            print("Invalid Amount")
            return
        
         addcredit_card(account,amount)
         print("Rs ",amount,"Credit card Added successfully");
    else:
        print("Sorry Account No doesn't match")



#date validation

def validate_date(date_from,date_to):
    pattern = "^[0-9]{1,2}-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)-([0-9]{4})$"
    if re.match(pattern,date_from) and re.match(pattern,date_to):
        date = date_from.split('-')
        if int(date[0]) > 0 and int(date[0]) <= 31 and int(date[2]) > 999:
            date2 = date_to.split('-')
            if int(date2[0]) > 0 and int(date2[0]) <= 31 and int(date2[2]) > 999:
                day_from = int(date[0])
                day_to = int(date2[0])
                mon_from = get_month(date[1])
                mon_to = get_month(date2[1])
                year_from = date[2]
                year_to = date2[2]
                if year_from < year_to:
                    return True
                elif year_from == year_to:
                    if mon_from < mon_to:
                        return True
                    elif mon_from == mon_to:
                        if day_from <= day_to:
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False

            else:
                return False
        else:
            return False
    else:
        return False

def get_month(month):
    if month == "jan":
        return 1
    elif month == "feb":
        return 2
    elif month == "mar":
        return 3
    elif month == "apr":
        return 4
    elif month == "may":
        return 5
    elif month == "jun":
        return 6
    elif month == "jul":
        return 7
    elif month == "aug":
        return 8
    elif month == "sep":
        return 9
    elif month == "oct":
        return 10
    elif month == "nov":
        return 11
    elif month == "dec":
        return 12        



def main():

    make_all_tables()
    reset_withdrawals()
    choice = 1

    while choice != 0:

        print("--- Main Menu --- ")
        print("1. Sign Up (New Customer) ")
        print("2. Sign In (Existing Customer) ")
        print("3. Admin Sign In ")
        print("0. Quit ")

        try:
            choice = int(input())

        except:
            print("Invalid Choice")
            choice = 1
            continue

        if choice == 1:
            sign_up();

        elif choice == 2:
            sign_in();
            
        elif choice == 3:
            admin_sign_in();
            

        elif choice == 0:
            print("Application Closed")

        else:
            print("Invalid Choice")

main()
