import psycopg2 as pg

def admin():
    while(True):
        print("---------OPTION--------")
        print("0. PRINT ALL CONTACTS")
        print("1. ADD NEW STUDENT")
        print("2. ADD CONTACT")
        print("3. MODIFY CONTACT")
        print("4. DELETE CONTACT")
        print("5. SPLIT EMAIL COLUMN")
        print("6. DOMAIN DISTRIBUTION VIEW")
        print("7. QUIT ADMIN MODE")
        print("-----------------------")

        command = input("OPTION? ")

        #0. PRINT ALL CONTACTS
        if command == '0':
            curs.execute("SELECT * FROM contacts, students WHERE contacts.sid = students.sid")
            for line in curs.fetchall():
                print(line)

        #1. ADD NEW STUDENT
        elif command == '1':
            curs.execute("INSERT INTO students VALUES ('2016001234', 'xxx', '홍길동', 'male', '6', '1999002345', '1')")
            conn.commit()

        #2. ADD CONTACT
        elif command == '2':
            curs.execute("INSERT INTO contacts VALUES ('2016001234','01088884444','hong@hanyang.ac.kr')")
            curs.commit()

        #3. MODIFY CONTACT
        elif command == '3':
            curs.execute("UPDATE contacts SET email='kwon@hanyang.ac.kr' WHERE sid = (SELECT s.sid FROM students s, contacts c WHERE s.sid=c.sid AND s.sname='권희조')")
            conn.commit()

        #4. DELETE CONTACT
        elif command == '4':
            curs.execute("DELETE FROM contacts WHERE sid = (SELECT s.sid FROM students s, contacts c WHERE s.sid=c.sid AND s.sname='김다현')")
            conn.commit()

        #5. SPLIT EMAIL COLUMN 
        elif command == '5':
            curs.execute("SELECT split_part(email, '@', 1) as local_part, split_part(email,'@',2) as domain_name FROM contacts")
            for line in curs.fetchall():
                print(line)

        #6. DOMAIN DISTRIBUTION VIEW
        elif command == '6':
            curs.execute("SELECT split_part(email,'@',2) as domain_name, COUNT (*) FROM contacts GROUP BY domain_name")
            for line in curs.fetchall():
                print(line)

        #7. QUIT ADMIN MODE
        elif command == '7':
            print("TERMINATE ADDRESS BOOK. BYE!")
            break

def student(login, passwd):

    if login in '2009003125':
        check = 1
    elif login in '2013004394':
        check = 2
    elif login in '2014005004':
        check = 3

    while(True):
        print("---------OPTION--------")
        print("1. ALL CONTACT LIST")
        print("2. ADD CONTACT")
        print("3. MODIFY CONTACT")
        print("4. DELETE CONTACT")
        print("5. QUIT")
        print("-----------------------")

        command = input("OPTION? ")

        #1. ALL CONTACT LIST
        if command == '1':
            print("HANYANG ADDRESS BOOK:")
            curs.execute("SELECT * FROM contacts")
            for line in curs.fetchall():
                print(line)
            print("")
            print("YOUR ADDRESS BOOK:")
            if(check == 1):
                curs.execute("SELECT * FROM grass_corp")
            elif(check == 2):
                curs.execute("SELECT * FROM fire_corp")
            elif(check == 3):
                curs.execute("SELECT * FROM water_corp")
            for line in curs.fetchall():
                print(line)
            
        #2. ADD CONTACT
        elif command == '2':
            if(check == 1):
                curs.execute("INSERT INTO grass_corp VALUES ('리피아',' 01061344185','leafeon@grass.poke','부장')")
                conn.commit()
            elif(check == 2):
                pass
            elif(check == 3):
                curs.execute("INSERT INTO water_corp VALUES ('마릴', ' 01029818318', 'marill@water.poke', '사원')")
                conn.commit()

        #3. MODIFY CONTACT
        elif command == '3':
            if(check == 1):
                curs.execute("UPDATE grass_corp SET name = '이상해풀', email = 'ivysaur@grass.poke', role = '이사' WHERE phone = ' 01023140011'")
                conn.commit()
                curs.execute("UPDATE grass_corp SET email = 'chikorita@grass.poke', role = '사장' WHERE phone = '01051522001'")
                conn.commit()
            elif(check == 2):
                curs.execute("UPDATE fire_corp SET name = '파이어로', email = 'talonflame@fire.poke', role = '대리' WHERE phone = ' 01066162014'")
                conn.commit()
            elif(check == 3):
                curs.execute("UPDATE water_corp SET name = '갸라도스', email = 'gyarados@water.poke', role = '과장' WHERE phone = ' 01091290760'")
                conn.commit()

        #4. DELETE CONTACT
        elif command == '4':
            if(check == 1):
                curs.execute("DELETE FROM grass_corp WHERE phone = ' 01032540033'")
                conn.commit()
            elif(check == 2):
                curs.execute("DELETE FROM fire_corp WHERE phone = ' 01086530042'")
                conn.commit()
            elif(check == 3):
                curs.execute("DELETE FROM water_corp WHERE phone = ' 01061344185'")
                conn.commit()
                curs.execute("DELETE FROM water_corp WHERE phone = ' 01029818318'")
                conn.commit()

        #6. QUIT
        elif command == '5':
            print("TERMINATE ADDRESS BOOK. BYE!")
            break

try:
    ##local DB connection
    conn_str = "host='localhost' dbname='postgres' user='postgres' password='kp2314uv'"
    conn = pg.connect(conn_str)
except:
    print("error: unable to connect to the database")
curs = conn.cursor()  


print("***HANYANG ADDRESS BOOK***")
login = input("id: ")
passwd = input("passwd: ")

if login == "admin":
    admin()
else:
    curs.execute("SELECT * FROM students")
    for line in curs.fetchall():
        if(login in line[0] and passwd in line[1]):
            student(login, passwd)