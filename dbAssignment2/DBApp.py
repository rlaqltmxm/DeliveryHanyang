import psycopg2 as pg
import json
import ast
from datetime import datetime as dt

order_states = ["before_delivery", "on_delivery", "delivery_completed", "cancelled"]

def seller(login):

    store_id = []

    print("Seller Login.")
    while(True):
        print("------OPTIONS------")
        print("0. My store")
        print("1. Modify name")
        print("2. Modify password")
        print("3. Terminate")
        print("-------------------")
        command = input("OPTION? ")

        if command == '0':
            print("*****STORE LIST*****")
            curs.execute("SELECT s2.sid, s2.sname, s2.phone_nums FROM seller s1, store s2 WHERE s1.local = %s AND s1.seller_id = s2.seller_id", [login])
            for line in curs.fetchall():
                print("Store ID: "+line[0]+"   / Name: "+line[1]+"  / Phones: ", end=" ")
                #print(line[2])
                for phones in json.loads(json.loads(line[2])):
                    print(phones,end=", ")
                print(" ")
            print("********************")

            while(True):
                print("0. Add menu")
                print("1. Modify menu")
                print("2. Delete menu")
                print("3. Now order list")
                print("4. Terminate")
                print("--------------------")
                command2 = input("OPTION? ")

                if command2 == '0':
                    sname = input("STORE NAME TO ADD MENU: ")
                    mname = input("MENU NAME TO BE ADDED: ")

                    curs.execute("SELECT sid FROM store WHERE name = %s", [sname])
                    sid = curs.fetchone()
                    curs.execute("INSERT INTO menu VALUES (%s, %s)", [mname, sid])
                    print("NEW MENU ADDED.")

                elif command2 == '1':
                    sname = input("STORE NAME TO MODIFY MENU: ")
                    mname = input("MENU NAME TO BE MODIFIED: ")
                    mname_updated = input("NEW MENU NAME: ")

                    curs.execute("SELECT sid FROM store WHERE name = %s", [sname])
                    sid = curs.fetchone()
                    curs.execute("UPDATE menu SET menu = %s WHERE sid = %s AND menu = %s",[mname_updated, sid, mname])
                    print("MENU UPDATED.")

                elif command2 == '2':
                    sname = input("STORE NAME TO DELETE MENU: ")
                    mname = input("MENU NAME TO BE DELETED: ")

                    curs.execute("SELECT sid FROM store WHERE name = %s", [sname])
                    sid = curs.fetchone()
                    curs.execute("DELETE FROM menu WHERE sid = %s AND menu = %s",[sid, mname])
                    print("MENU DELETED.")

                elif command2 == '3':
                    order_cnt = 0
                    sname = input("STORE NAME TO GET ORDER LIST: ")

                    curs.execute("SELECT sid FROM store WHERE sname = %s", [sname])
                    sid = curs.fetchone()
                    curs.execute("SELECT state, sid, menu, cus_id, CAST(ordertime AS TIME) FROM orders WHERE sid = %s", [sid])
                    print("*****ORDER LIST*****")           
                    for line in curs.fetchall():
                        print("("+line[0]+")Store ID: "+line[1]+"  / Menu: "+line[2]+" / Customer ID: "+line[3]+"  / Order Time: "+str(line[4]))
                        order_cnt += 1
                    print("********************")
                    print("0. Do nothing")
                    print("1. Check order")
                    print("2. Cancel order")
                    print("********************")
                    command3 = input("OPTION? " )

                    if command3 == '0': pass

                    elif command3 == '1':

                        curs.execute("SELECT d.did, d.name, d.phone, d.stock FROM delivery d, store s WHERE ABS(CAST(s.lat AS FLOAT)-CAST(d.lat AS FLOAT)) < 0.1 AND ABS(CAST(s.lng AS FLOAT)-CAST(d.lng AS FLOAT)) < 0.1 AND CAST(stock AS INT) <= 4 LIMIT 5")
                        print("****DELIVERY LIST****")           
                        for line in curs.fetchall():
                            print("Delivery ID: "+line[0]+"  / Name: "+line[1]+"    / Phone: "+line[2]+"    / Now Stock: "+line[3])
                        print("*********************")
                        command4 = input("DELIVERY ID TO GIVE ORDER: ")

                        for i in range(order_cnt):
                            curs.execute("UPDATE orders SET did = %s, state = %s WHERE sid = %s", [command4, order_states[1], sid])
                        print("ORDERS NOW ON DELIVERY.")
                            
                    elif command3 == '2':
                        curs.execute("UPDATE orders SET state = %s WHERE sid = %s", [order_states[3], sid])
                        print("ORDERS CANCELLED.")

                elif command2 == '4':
                    break

        elif command == '1':
            name = input("New name: ")
            curs.execute("UPDATE seller SET name = %s WHERE local = %s", (name, login))
            print("Your name updated.")

        elif command == '2':
            name = input("New password: ")
            curs.execute("UPDATE seller SET passwd = %s WHERE local = %s", (passwd, login))
            print("Your password updated.")

        elif command == '3':
            break

def customer(login):

    print("Customer Login.")
    order_cnt = 0
    addresses = []
    while(True):
        print("------OPTIONS------")
        print("0. Make order")
        print("1. My order")
        print("2. Modify name")
        print("3. Modify password")
        print("4. My address book")
        print("5. My payments")
        print("6. Terminate")
        print("-------------------")
        command = input("OPTION? ")

        if command == '0':
            
            print("*****NEAR STORES OPENING*****")
            curs.execute("SELECT s.sname, s.phone_nums FROM store s, customer c WHERE c.local = %s AND ABS(CAST(s.lat AS FLOAT)-CAST(c.lat AS FLOAT)) < 0.1 AND ABS(CAST(s.lng AS FLOAT)-CAST(c.lng AS FLOAT)) < 0.1 LIMIT 20", [login])
            for line in curs.fetchall():
                print("Store Name: "+line[0]+"  / Phones: ", end=" ")
                #print(line[2])
                for phones in json.loads(json.loads(line[1])):
                    print(phones,end=", ")
                print(" ")
            print("*****************************")
            
            sname = input("STORE NAME: ")
            print("****MENU OF "+sname+" ****")
            curs.execute("SELECT m.menu FROM menu m, store s WHERE s.sname = %s AND m.sid = s.sid", [sname])
            for line in curs.fetchall():
                print(line[0])
            print("**************************")

            mname = input("MENU NAMES(name1,name2,...): ")
            m_split = mname.split(",")

            curs.execute("SELECT payments FROM customer WHERE local = %s", [login])
            pay_info = ast.literal_eval(curs.fetchone()[0])
            print("*****MY PAYMENTS*****")
            cnt = 0
            for i in pay_info:
                cnt += 1
                i['data'] = ast.literal_eval(i['data'])
                if i['type'] == 'account':
                    print("#"+str(cnt)+" Bank ID: "+str(i['data']["bid"])+" / Account Num: "+str(i['data']["acc_num"]))
                elif i['type'] == 'card':
                    print("#"+str(cnt)+" Card Num: "+str(i['data']["card_num"]))
                i['data'] = str(i['data'])
            print("*********************")

            py = input("SELECT PAYMENT #: ")

            ppy = ""
            for i in pay_info:
                cnt += 1
                if i['type'] == 'account':
                    ppy = "account"
                elif i['type'] == 'card':
                    ppy = "card"

                if cnt == int(py): break

            print("PAYMENT COMPLETED.")

            for i in range(len(m_split)):
                state = order_states[0]
                curs.execute("SELECT sid FROM store WHERE sname = %s", [sname])
                sid = curs.fetchone()
                did = "-1"
                curs.execute("SELECT phone FROM customer WHERE local = %s", [login])
                cus_phone = curs.fetchone()
                
                payments = ppy
                ordertime = dt.now()

                curs.execute("INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [state, sid, m_split[i], did, login, cus_phone, payments, ordertime])            
                order_cnt += 1
                print("NEW ORDER "+str(order_cnt)+" MADE.")

        elif command == '1':
            print("*****ORDER LIST*****")
            curs.execute("SELECT state, sid, menu, CAST(ordertime AS TIME) FROM orders WHERE cus_id = %s", [login])
            for line in curs.fetchall():
                print("("+line[0]+")Store ID: "+line[1]+"  / Menu: "+line[2]+" / Order Time: "+str(line[3]))
            print("********************")
            print("0. Do nothing")
            print("1. Complete order")
            print("2. Cancel order")
            print("********************")

            command2 = input("OPTION? ")
            if command2 == '0':
                pass                

            elif command2 == '1':

                for i in range(order_cnt):
                    curs.execute("UPDATE orders SET payments = %s WHERE cus_id = %s", [order_states[2], login])
                print("ORDERS ALL PAYED.")
                
            elif command2 == '2':
                for i in range(order_cnt):
                    curs.execute("UPDATE orders SET state = %s WHERE cus_id = %s", [order_states[3], login])
                print("ORDERS ALL CANCELLED.")

        elif command == '2':
            name = input("New name: ")
            curs.execute("UPDATE customer SET name = %s WHERE local = %s", (name, login))
            print("Your name updated.")

        elif command == '3':
            name = input("New password: ")
            curs.execute("UPDATE customer SET passwd = %s WHERE local = %s", (passwd, login))
            print("Your password updated.")

        elif command == '4':
            if len(addresses) == 0:
                print("NO ADDRESS EXSITS.")
            else:
                for i in range(len(addresses)):
                    print("Add #"+str(i)+" "+addresses[i])

            while(True):
                print("****MY ADDRESS BOOK****")
                print("0. Add address")
                print("1. Modify address")
                print("2. Delete address")
                print("3. Terminate")
                print("***********************")
                command0 = input("OPTION? ")
                if command0 == '0':
                    commandd = input("NEW ADDRESS: ")
                    addresses.append(commandd)
                    print("Address book Updated.")

                elif command0 == '1':
                    commandd = input("ADDRESS NUM TO MODIFY")
                    comm = input("UPDATED ADDRESS: ")
                    addresses[addresses.index(commandd-1)] = comm
                    print("Address book Updated.")
                elif command0 == '2':
                    commandd = input("ADDRESS NUM TO DELETE: ")
                    del addresses[addresses.index(commandd-1)]
                    print("Address book Updated.")
                elif command0 == '3':
                    break

        elif command == '5':
            curs.execute("SELECT payments FROM customer WHERE local = %s", [login])
            pay_info = ast.literal_eval(curs.fetchone()[0])

            cnt = 0
            print("****PAYMENT LIST****")
            for i in pay_info:
                cnt += 1
                i['data'] = ast.literal_eval(i['data'])
                if i['type'] == 'account':
                    print("#"+str(cnt)+" Bank ID: "+str(i['data']["bid"])+" / Account Num: "+str(i['data']["acc_num"]))
                elif i['type'] == 'card':
                    print("#"+str(cnt)+" Card Num: "+str(i['data']["card_num"]))
                i['data'] = str(i['data'])
            print("*********************")

        elif command == '6':
            break

def delivery(login):
    print("Delivery Login.")
    while(True):
        print("------OPTIONS------")
        print("0. My order")
        print("1. Modify name")
        print("2. Modify password")
        print("3. Terminate")
        print("-------------------")
        command = input("OPTION? ")

        if command == '0':

            curs.execute("SELECT did FROM delivery WHERE local = %s", [login])
            did = curs.fetchone()
            print("*****ORDER LIST*****")
            curs.execute("SELECT state, sid, menu, cus_id, payments, cus_phone, CAST(ordertime AS TIME) FROM orders WHERE did = %s", [did])
            for line in curs.fetchall():
                print("("+line[0]+")Store ID: "+line[1]+"   / Menu: "+line[2]+" / Cus_ID: "+line[3]+" / Payments: "+line[4]+" / Cus_phone: "+line[5]+" / Order Time: "+str(line[6]))
            print("********************")

        elif command == '1':
            name = input("New name: ")
            curs.execute("UPDATE delivery SET name = %s WHERE local = %s", (name, login))
            print("Your name updated.")

        elif command == '2':
            name = input("New password: ")
            curs.execute("UPDATE delivery SET passwd = %s WHERE local = %s", (passwd, login))
            print("Your password updated.")

        elif command == '3':
            break

try:
    ##local DB connection
    conn_str = "host='localhost' dbname='postgres' user='postgres' password='kp2314uv'"
    conn = pg.connect(conn_str)
    conn.autocommit = True
except:
    print("error: unable to connect to the database")

curs = conn.cursor()

#order table initialize
curs.execute("DROP TABLE IF EXISTS orders")
curs.execute("CREATE TABLE orders ( state VARCHAR, sid VARCHAR, menu VARCHAR, did VARCHAR, cus_id VARCHAR, cus_phone VARCHAR, payments VARCHAR, ordertime TIMESTAMP, FOREIGN KEY (sid) REFERENCES store(sid) )")

while(True):

    print("***HANYANG DELIVERY***")
    email = input("email: ")
    passwd = input("passwd: ")

    check = 0

    eemail = email.split('@')
    local = eemail[0]
    domain = eemail[1]

    curs.execute("SELECT * FROM seller")
    for line in curs.fetchall():
        if local in line[3] and domain in line[4] and passwd in line[5]:
            seller(local)
            check = 1
            break

    curs.execute("SELECT * FROM customer")
    for line in curs.fetchall():
        if local in line[2] and domain in line[3] and passwd in line[4]:
            customer(local)
            check = 1
            break

    curs.execute("SELECT * FROM delivery")
    for line in curs.fetchall():
        if local in line[3] and domain in line[4] and passwd in line[5]:
            delivery(local)
            check = 1
            break

    if check == 0:
        print("INVALID ACCOUNT. PLEASE RETRY")
    elif check == 1:
        print("******GOOD BYE!******")
        continue

curs.close()
conn.close()