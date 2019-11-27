import psycopg2
import names
import datetime
import random

conn_string = "host='localhost' dbname='hospital' user='postgres' password=''"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
equipment = ['vacuum cleaner', 'X-Ray', 'thermometer', 'test-tube', 'robe', 'defibrillator', 'scalpel', 'stethoscope']
roles = ['doctor', 'nurse', 'receptionist', 'seller', 'primary doctor', 'staff']
passwords = ['pswrd1', 'asdjwekfb', 'asdwwqeqwe', 'jgh6ryh', 'gr34g24c', 'zxfgew2', 'hy43fgb5', 'pashbk334w']
genders = ['male', 'female', 'other']
streets = ['Moiwa st.', 'Tea st.', 'Imagination st.', 'Kojima st.', 'Mob st.', 'Main st.', 'LoveMyself st.',
           'Street st.']
offices = []
ssns = []
appointments=[]
notifications = []
slots=['0:00','1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00','19:00','20:00','21:00','22:00','23:00']
drugs = ["Supermedicine", 'MegaMedicine', 'GoodMedicine', 'Medicinetol']
messages = ['Hey, wanna go to the bar today?', 'Our life with database became much easier!']
illnesses = ['cancer', 'not cancer', 'crab-hands', 'horsehead', 'centaurism', 'octohandism', 'imaginary illness']
cursor.execute("delete from billcontainsdrugs;")
cursor.execute("delete from receiptcontainsdrugs;")
cursor.execute("delete from equipmentusedbystaff;")
cursor.execute("delete from workdaystaff;")
cursor.execute("Delete from notification;")
cursor.execute("Delete from appointment;")
cursor.execute("Delete from receipt;")
cursor.execute("Delete from drug;")
cursor.execute("Delete from weekday;")
cursor.execute("Delete from bill;")
cursor.execute("Delete from Equipment;")
cursor.execute("Delete from Message;")
cursor.execute("Delete from Staff;")
cursor.execute("Delete from Bill;")
cursor.execute("Delete from Report ;")
cursor.execute("Delete from MedicalHistoryItem ;")
cursor.execute("Delete from Patient;")
num_of_equip=8
num_of_staff=100
num_of_patients=40
num_of_medical_history_items=50
num_of_reports=50
num_of_messages=156
num_of_bills=79
num_of_drugs=4
num_of_receipts=20
num_of_appointments=3000
num_of_notifications=37
for i in range(400):
    offices.append(i)                   #append values to offices and ssns lists
    ssns.append(i)


def insertDaysOfWeek():
    for i in range(0, 7, 1):
        cursor.execute(f"INSERT INTO WEEKDAY VALUES ('{days[i]}');")    #insert weekdays into database


def insertEquipment():
    for i in range(num_of_equip):
        equip = random.choice(equipment)                        #chose random name of equipment
        cursor.execute(
            f"INSERT INTO Equipment(name,quantity) Values ('{equip}',{random.randint(1, 9)});") #insert equipment with random quantity
        equipment.remove(equip)     #remove from list to avoid repeatings


def insertStaff():
    for i in range(num_of_staff):
        ssn = random.choice(ssns)                           #first initialize all values
        ssns.remove(ssn)
        office = random.choice(offices)
        offices.remove(office)
        if i == 0:
            role_id = 'primary doctor'                  # there should be only one primary doctor
        else:
            if i == 1:
                role_id = 'seller'                      #at least one seller
            else:
                if i==2:
                    role_id='receptionist'              #and at least one receptionist
                else:
                    role_id = random.choice(roles)
        hiring_date = datetime.date(random.randint(2000, 2019), random.randint(1, 12), random.randint(1, 28)) #randomize all values
        salary = random.randint(30000, 60000)
        password = random.choice(passwords)
        first_name=names.get_first_name('any')
        last_name = names.get_last_name()
        birthdate = datetime.date(random.randint(1950, 1980), random.randint(1, 12), random.randint(1, 28))
        cursor.execute(
            f"INSERT INTO Staff(ssn,role_id,office,hiring_date,salary,password,first_name,last_name,birthday) Values({ssn},'{role_id}',{office},TIMESTAMP '{hiring_date}',{salary},'{password}','{first_name}','{last_name}',TIMESTAMP '{birthdate}')")
        if role_id == 'primary doctor':
            roles.remove(role_id)


def insertPatient():
    for i in range(num_of_patients):
        insurance = random.choice(ssns)                                     #first we initialize values randomly
        ssns.remove(insurance)
        name = names.get_full_name('any')
        birthdate = datetime.date(random.randint(1912, 1999), random.randint(1, 12), random.randint(1, 28))
        gender = random.choice(genders)
        address = random.choice(streets)
        password = random.choice(passwords)
        cursor.execute(
            f"INSERT INTO Patient(medical_insurance_id,name,birthday,gender,address,password) values({insurance},"
            f"'{name}', TIMESTAMP '{birthdate}','{gender}','{address}','{password}');")


def getPatientId():
    cursor.execute("Select medical_insurance_id from Patient;")
    i = 0
    num = random.randint(0, num_of_patients-1)
    for row in cursor:
        if i == num:
            return row[0]       #get 0th attribute from the random patient
        i += 1


def insertMedicalHistoryItem():
    for i in range(num_of_medical_history_items):
        patient_id = getPatientId()
        cursor.execute(f"Select birthday from Patient where medical_insurance_id={patient_id}")
        for row in cursor:
            dateOfB = row[0]
        start = datetime.date(random.randint(2000, 2019), random.randint(1, 12), random.randint(1, 28))
        symptoms = "Have a nice day! Try to enjoy it..."
        diagnosis = random.choice(illnesses)
        extra = "Extra info"
        if random.randint(0, 2) == 1:
            end = datetime.date(random.randint(start.year, 2019), random.randint(1, 12), random.randint(1, 28))
            cursor.execute(
                f"Insert into MedicalHistoryItem(start_of_illness,end_of_illness,symptoms,diagnosis,extra_info,patient_id) "
                f"values (TIMESTAMP '{start}',TIMESTAMP '{end}','{symptoms}','{diagnosis}','{extra}',{patient_id})")
        else:
            cursor.execute(
                f"Insert into MedicalHistoryItem(start_of_illness,symptoms,diagnosis,extra_info,patient_id) "
                f"values (TIMESTAMP '{start}','{symptoms}','{diagnosis}','{extra}',{patient_id})")


def getMHI(id):
    cursor.execute(f"Select id from MedicalHistoryItem where MedicalHistoryitem.patient_id={id};")
    i = 0
    for row in cursor:              #count MHIs of patient with given id
        i += 1
    j = random.randint(0, i)
    i = 0
    cursor.execute(f"Select id from MedicalHistoryItem where MedicalHistoryitem.patient_id={id};")
    for row in cursor:
        if i == j:
            return row[0]
        i += 1


def insertReport():
    for i in range(num_of_reports):
        content = "This is report about illness"
        id = getPatientId()
        mhi = getMHI(id)
        if mhi != None:                             #if report has medical history item, then add it
            cursor.execute(f"Insert into Report(content,patient_id,medical_history_item_id) values"
                           f"('{content}',{id},{mhi});")
        else:                                                  #otherwise add without mhi
            cursor.execute(f"Insert into Report(content,patient_id) values"
                           f"('{content}',{id});")


def getStaffId():
    cursor.execute("Select ssn from Staff;")
    i = 0
    num = random.randint(0, 14)
    for row in cursor:
        if i == num:
            return row[0]
        i += 1


def insertMessage():
    for i in range(num_of_messages):
        receiver = getStaffId()
        sender = getStaffId()
        content = random.choice(messages)
        cursor.execute(f"Insert into message(receiver_id,sender_id,content) values"
                       f"({receiver},{sender},'{content}')")


def insertBill():
    for i in range(num_of_bills):
        seller = getSeller()
        patient = getPatientId()
        issued=datetime.datetime(random.randint(2019,2022),random.randint(1,12),random.randint(1,28),0,0,0)
        cursor.execute(f"Insert into Bill(issued_date,seller_id,patient_id) values"
                       f"(TIMESTAMP '{issued}',{seller},{patient})")


def getSeller():
    cursor.execute("Select ssn from Staff where Staff.role_id='seller';")
    i = 0
    for row in cursor:
        i += 1
    num = random.randint(0, i - 1)
    cursor.execute("Select ssn from Staff where Staff.role_id='seller';")
    i = 0
    for row in cursor:
        if i == num:
            return row[0]
        i += 1


def insertDrug():
    for i in range(num_of_drugs):
        quantity = random.randint(1, 25)
        expire = datetime.date(random.randint(2019, 2030), random.randint(1, 12), random.randint(1, 28))
        name = random.choice(drugs)
        drugs.remove(name)
        cost = random.randint(500, 5000)
        cursor.execute(f"Insert into drug(quantity_in_stock,expire_date,name,cost) values"
                       f"({quantity},TIMESTAMP '{expire}','{name}',{cost});")


def insertReceipt():
    for i in range(num_of_receipts):
        validity = datetime.date.today()
        if validity.month != 12:
            validity = datetime.date(validity.year, validity.month + 1, validity.day)
        else:
            validity = datetime.date(validity.year + 1, 1, validity.day)
        patient = getPatientId()
        doctor = getDoctorId()
        used = False
        if random.randint(0, 2) == 1:
            used = True;
        cursor.execute(f"Insert into receipt(is_used,validity_end_date,patient_id,doctor_id) values"
                       f"({used},TIMESTAMP '{validity}',{patient},{doctor})")


def getDoctorId():
    cursor.execute("Select ssn from Staff where Staff.role_id='doctor' or Staff.role_id='primary doctor';")
    i = 0
    for row in cursor:
        i += 1
    num = random.randint(0, i - 1)
    cursor.execute("Select ssn from Staff where Staff.role_id='doctor' or Staff.role_id='primary doctor';")
    i = 0
    for row in cursor:
        if i == num:
            return row[0]
        i += 1


def insertAppointment():
    for i in range(num_of_appointments):
        patient = getPatientId()
        doctor = getDoctorId()
        date = datetime.date(random.randint(2010, 2019), random.randint(1, 12), random.randint(1, 28))
        slot = random.choice(slots)
        if (doctor,date,slot) not in appointments:          #check that key is unique

            cursor.execute(f"Insert into appointment(patient_id,doctor_id,date,slot) values"
                           f"({patient},{doctor},TIMESTAMP '{date}','{slot}');")
            appointments.append((doctor, date, slot))


def insertNotification():

    for i in range(num_of_notifications):
        date = datetime.datetime(random.randint(2020, 2022), random.randint(1, 12), random.randint(1, 28),
                                 random.randint(8, 18), random.randint(0, 59))
        patient = getPatientId()
        receptionist = getReceptionist()
        content = "You have to do something"
        if (patient,date) not in notifications:             #check that key is unique
            cursor.execute(f"Insert into Notification(patient_id,receptionist_id,datetime,content) values"
                           f"({patient},{receptionist},TIMESTAMP'{date}','{content}')")
            notifications.append((patient,date))

def getReceptionist():
    cursor.execute("Select ssn from Staff where Staff.role_id='receptionist';")
    i = 0
    for row in cursor:
        i += 1
    num = random.randint(0, i - 1)
    cursor.execute("Select ssn from Staff where Staff.role_id='receptionist';")
    i = 0
    for row in cursor:
        if i == num:
            return row[0]
        i += 1


def insertWorkDays():
    staffIds = []
    copyStaff(staffIds)
    for i in range(num_of_staff):
        st = random.choice(staffIds)
        staffIds.remove(st)
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for j in range(4):
            day = random.choice(days)
            days.remove(day)        #in this and next methods all the keys are unique
            cursor.execute(f"Insert into workdaystaff(day_name,staff_ssn) values"
                           f"('{day}',{st});")


def insertEUBS():
    list = []
    copyStaff(list)
    for i in range(num_of_staff):
        st = random.choice(list)
        list.remove(st)
        equipment = ['vacuum cleaner', 'X-Ray', 'thermometer', 'test-tube', 'robe', 'defibrillator', 'scalpel',
                     'stethoscope']
        for j in range(random.randint(0, 6)):
            eq = random.choice(equipment)
            equipment.remove(eq)
            cursor.execute(f"Insert into EquipmentUsedByStaff(equipment_id,staff_ssn,quantity) values"
                           f"({getEquip(eq)},{st},{random.randint(1, 4)})")


def copyStaff(ar):
    cursor.execute("Select ssn from Staff;")
    for row in cursor:
        ar.append(row[0])


def getEquip(a):
    cursor.execute(f"Select id from Equipment where Equipment.name='{a}'")
    for row in cursor:
        return row[0]


def insertBillContainsDrugs():
    bills = []
    copyBills(bills)
    for i in range(random.randint(0, 23)):
        bill = random.choice(bills)
        bills.remove(bill)
        drugs = []
        copyDrugs(drugs)
        for j in range(random.randint(0, 4)):
            drug = random.choice(drugs)
            drugs.remove(drug)
            cursor.execute(f"Insert into billcontainsdrugs(bill_id,drug_id,quantity) values"
                           f"({bill},{drug},{random.randint(1, 3)})")


def insertReceiptContainsDrugs():
    receipts = []
    copyReceipts(receipts)
    for i in range(random.randint(0, 20)):
        receipt = random.choice(receipts)
        receipts.remove(receipt)
        drugs = []
        copyDrugs(drugs)
        for j in range(random.randint(0, 4)):
            drug = random.choice(drugs)
            drugs.remove(drug)
            cursor.execute(f"Insert into receiptcontainsdrugs(receipt_id,drug_id,quantity) values"
                           f"({receipt},{drug},{random.randint(1, 3)})")


def copyBills(ar):
    cursor.execute(f"Select id from bill;")
    for row in cursor:
        ar.append(row[0])


def copyReceipts(ar):
    cursor.execute(f"Select id from receipt;")
    for row in cursor:
        ar.append(row[0])


def copyDrugs(ar):
    cursor.execute(f"Select id from drug;")
    for row in cursor:
        ar.append(row[0])


insertDaysOfWeek()
insertEquipment()
insertStaff()
insertPatient()
insertMedicalHistoryItem()
insertReport()
insertMessage()
insertBill()
insertDrug()
insertReceipt()
insertAppointment()
insertNotification()
insertWorkDays()
insertEUBS()
insertBillContainsDrugs()
insertReceiptContainsDrugs()
conn.commit()
conn.close()
