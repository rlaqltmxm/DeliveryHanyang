import csv

with open('students.csv', 'r', encoding='utf-8') as f1:
    cstudents = csv.reader(f1)
    students = list(cstudents)
with open('contacts.csv', 'r', encoding='utf-8') as f2:
    ccontacts = csv.reader(f2)
    contacts = list(ccontacts)

def admin():
    while(True):
        print("---------OPTION--------")
        print("0. PRINT ALL CONTACTS")
        print("1. ADD NEW STUDENT")
        print("2. ADD CONTACT")
        print("3. MODIFY CONTACT")
        print("4. DELETE CONTACT")
        print("5. SPLIT EMAIL COLUMN")
        #print("5. DOMAIN DISTRIBUTION VIEW")
        print("6. QUIT ADMIN MODE")
        print("-----------------------")

        command = input("OPTION? ")

        if command == '0':
            for line in contacts:
                print(line)

        elif command == '1':
            input_str = "2016001234,XXX,홍길동,male,6,1999002345,1"
            students.append(input_str.split(","))

        elif command == '2':
            input_str = "2016001234,01088884444,hong@hanyang.ac.kr"
            contacts.append(input_str.split(","))

        elif command == '3':
            sid = ""
            for student in students:
                if "권희조" in student[2]:
                    sid = student[0]
                    break
            
            for contact in contacts:
                if contact[0] == sid:
                    contact[2] = "kwon@hanyang.ac.kr"
                    break

        elif command == '4':
            sid = ""
            for student in students:
                if "김다현" in student[2]:
                    sid = student[0]
                    break

            for i in range(len(contacts)):
                if contacts[i][0] == sid:
                    contacts.remove(contacts[i])
                    break

        elif command == '5':
            for contact in contacts:
                email = contact[2]
                split = email.split("@")
                print(split)

        elif command == '6':
            print("TERMINATE ADDRESS BOOK. BYE!")
            break

def stud(login, passwd):

    indiv_contact = []

    #initialize 3 students
    for student in students:
        if login in student[0]:
            if "정남아" in student[2]:
                with open("Grass_corp.csv", 'r', encoding='utf-8') as f:                        
                    cindiv_contact = csv.reader(f)
                    indiv_contact = list(cindiv_contact)
                    f.close()
                
            elif "윤인욱" in student[2]:
                with open("Fire_corp.csv", 'r', encoding='utf-8') as f:
                    cindiv_contact = csv.reader(f)
                    indiv_contact = list(cindiv_contact)
                    f.close()
                
            elif "장두호" in student[2]:
                with open("Water_corp.csv", 'r', encoding='utf-8') as f:
                    cindiv_contact = csv.reader(f)
                    indiv_contact = list(cindiv_contact)
                    f.close()    
            break

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
            print("HANYANG ADDRESS BOOK")
            for contact in contacts:
                print(contact)
            print("")
            print("YOUR ADDRESS BOOK")
            for indiv in indiv_contact:
                print(indiv)

        #2. ADD CONTACT
        elif command == '2':
            for student in students:
                if login in student[0]:
                    if "정남아" in student[2]:
                        input_str = "리피아,01061344185,leafeon@grass.poke,부장"      
                        indiv_contact.append(input_str.split(","))
                        break

                    elif "윤인욱" in student[2]:
                        break

                    elif "장두호" in student[2]:
                        input_str = "마릴,01029818318,marill@water.poke,사원"
                        indiv_contact.append(input_str.split(","))
                        break

        #3. MODIFY CONTACT
        elif command == '3':
            for student in students:
                if login in student[0]:
                    if "정남아" in student[2]:
                        for i in range(len(indiv_contact)):
                            if "01023140011" in indiv_contact[i][1]:
                                updated = "이상해풀,01023140011,ivysaur@grass.poke,이사"
                                indiv_contact[i] = updated.split(",")
                            elif "01051522001" in indiv_contact[i][1]:
                                updated = "치코리타,01051522001,meganium@grass.poke,사장"
                                indiv_contact[i] = updated.split(",")

                    elif "윤인욱" in student[2]:
                        for i in range(len(indiv_contact)):
                            if "01066162014" in indiv_contact[i][1]:
                                updated = "파이어로,01066162014,alonflame@fire.poke,대리"
                                indiv_contact[i] = updated.split(",")

                    elif "장두호" in student[2]:
                        for i in range(len(indiv_contact)):
                            if "01091290760" in indiv[i][1]:
                                updated = "갸라도스,01091290760,gyarados@water.poke,과장"
                                indiv_contact[i] = updated.split(",")

        #4. DELETE CONTACT
        elif command == '4':
            for student in students:
                if login in student[0]:
                    if "정남아" in student[2]:
                        bye = indiv_contact.pop()
                        break

                    elif "윤인욱" in student[2]:
                        bye = indiv_contact.pop()
                        break

                    elif "장두호" in student[2]:
                        for i in range(len(indiv_contact)):
                            if "01061344185" in indiv_contact[i][1]:
                                indiv_contact.remove(indiv_contact[i])
                        bye = indiv_contact.pop()
                        break

        #6. QUIT
        elif command == '5':
            print("TERMINATE ADDRESS BOOK. BYE!")
            break



print("***HANYANG ADDRESS BOOK***")
login = input("id: ")
passwd = input("passwd: ")

if login == "admin":
    admin()

else:
    for student in students:
        if login in student[0] and passwd in student[1]:
            stud(login, passwd)
            break

f1.close()
f2.close()