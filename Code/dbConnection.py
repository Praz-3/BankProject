import pymysql

con = pymysql.connect(host='localhost', user='root', password='root', db='infosys_robMe_bank')
cur = con.cursor()
