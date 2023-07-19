
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

def tableOutput(dataArray):
    punches = dataArray[0]
    attendancedate = dataArray[1]
    employeeid = dataArray[2]
    attendancelogid = dataArray[3]

    employee_id = []
    attendance_log_id = []
    attendance_dates = []
    insArray = []
    outsArray = []

    arrayOfinOuts = punches.split(",")

    allsorteddata = []

    for i in range(len(arrayOfinOuts)):
        if arrayOfinOuts.index(arrayOfinOuts[i]) == i:
            allsorteddata.append(arrayOfinOuts[i])

    arrayOfinOuts = allsorteddata

    inCons = 0
    outsCons = 0

    for inouts in arrayOfinOuts:
        if "in" in inouts and inCons == 0:
            insArray.append(inouts)
            inCons += 1
            outsCons = 0
        elif "in" in inouts and inCons > 0:
            insArray.append(inouts)
            outsArray.append('')
        elif "out" in inouts and outsCons == 0:
            outsArray.append(inouts)
            outsCons += 1
            inCons = 0
        elif "out" in inouts and outsCons > 0:
            outsArray.append(inouts)
            insArray.append('')

    updatedins = []
    updatedouts = []

    for i in insArray:
        a = i.split(":")
        updatedins.append(':'.join(a[:2]))

    for i in outsArray:
        a = i.split(":")
        updatedouts.append(':'.join(a[:2]))

    insArray = updatedins
    outsArray = updatedouts

    grtLen = 0

    if len(insArray) >= len(outsArray):
        grtLen = len(insArray)
    else:
        grtLen = len(outsArray)

    for i in range(grtLen):
        attendance_dates.append(attendancedate)
        employee_id.append(employeeid)
        attendance_log_id.append(attendancelogid)

    if len(insArray) == len(outsArray):
        pass
    elif len(insArray) > len(outsArray):
        outsArray.append('')
    else:
        insArray.append('')

    punch_in_times = insArray
    punch_out_times = outsArray

    # Create pandas DataFrame
    punch_df = pd.DataFrame({'employee_id': employee_id,'attendance_log_id': attendance_log_id, 'attendance_date': attendance_dates, 'punch_in': ["" if x == '' else x for x in punch_in_times], 'punch_out': ["" if x == '' else x for x in punch_out_times]})


    # Convert employee_id to int type
    punch_df['employee_id'] = punch_df['employee_id'].astype(int)

    # Display output
    return punch_df

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sys"
)

# Create SQLAlchemy engine object using the MySQL connector object
engine = create_engine('mysql+mysqlconnector://root:root@localhost/sys')

# Define MySQL query
query = "SELECT employee_id, attendance_log_id, attendance_date, punch_records FROM stg_attendancelogs WHERE attendance_log_id NOT IN (SELECT attendance_log_id FROM dim_attendance_records)"

# Execute MySQL query and read results into pandas DataFrame
df = pd.read_sql_query(query, engine)

# Create empty lists for punch in and out times and attendance dates


allPunches=[]
allDates=[]
allEmployes=[]
alllogs = []

for punchrecs in df['punch_records']:
    allPunches.append(punchrecs)
for attendanceDate in df['attendance_date']:
    allDates.append(attendanceDate)
for employeeId in df['employee_id']:
    allEmployes.append(employeeId)
for attendancelogid in df['attendance_log_id']:
    alllogs.append(attendancelogid)

allData=[]

for i in range(len(allPunches)):
    if allPunches[i]!="":
        allData.append([allPunches[i], allDates[i], allEmployes[i], alllogs[i]])
        
data = {'employee_id':  [""],
        'attendance_log_id':  [""],
        'attendance_date': [""],
        'punch_in': [None],
        'punch_out': [None]
        }
allDataMerged=pd.DataFrame(data)
        
for j in allData:
    allDataMerged= pd.concat([allDataMerged, tableOutput(j)])
    

allDataMerged.reset_index(inplace = True, drop = True)
allDataMerged.drop(index=0, inplace = True)


# print(allDataMerged)
# print(allDataMerged.head(50))
# Save output DataFrame to MySQL database
cursor = db.cursor()
for i, row in allDataMerged.iterrows():
    cursor.execute("INSERT INTO dim_attendance_records (employee_id, attendance_log_id, attendance_date, punch_in, punch_out) VALUES (%s, %s, %s, %s, %s)", (row['employee_id'],row['attendance_log_id'], row['attendance_date'], row['punch_in'], row['punch_out']))
db.commit()
db.close()


