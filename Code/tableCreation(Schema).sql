use infosys_robMe_bank;
create table customers(
                  customer_id int primary key AUTO_INCREMENT,
                  first_name varchar(10),
                  last_name varchar(10),
                  status varchar(10),
                  login_attempts int,
                  password varchar(20));
create table address(
                  customer_id int,
                  line1 varchar(30),
                  line2 varchar(30),
                  city varchar(30),
                  state varchar(30),
                  pincode int,
                  constraint fk_addr foreign key(customer_id) references customers(customer_id));
                  
create table accounts(
                  customer_id int,
                  account_no int primary key,
                  opened_on date,
                  account_type varchar(10),
                  status varchar(10),
                  balance int,
                  withdrawals_left int,
                  constraint fk_acc foreign key(customer_id) references customers(customer_id));
                  
create table closed_accounts(
                  account_no int,
                  closed_on date,
                  constraint fk_closed_acc foreign key(account_no) references accounts(account_no));
                  
create table transactions(
                  transaction_id int primary key,
                  account_no int,
                  type varchar(10),
                  amount int,
                  balance bigint,
                  transaction_date date,
                  constraint fk_transaction_account_no foreign key(account_no) references accounts(account_no));