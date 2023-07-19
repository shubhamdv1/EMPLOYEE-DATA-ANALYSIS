import mysql.connector
import pandas as pd
from datetime import datetime
from datetime import timedelta
from sqlalchemy import create_engine


def tableOutput(dataArray):
    punches = dataArray[0].split(",")
    attendancedate = dataArray[1]
    employeeid = dataArray[2]
    attendancelogid = dataArray[3]
    newPunches=[]

    employee_id = []
    attendance_log_id = []
    attendance_dates = []
    insArray = []
    outsArray = []
    
    coins=0
    couots=0
    
    for k in range(len(punches)):
        if k ==punches.index(punches[k]) and punches[k]!="":
            newPunches.append(punches[k])
            
    punches = newPunches

    for i in punches:
        if punches.index(i)==0:
            if "in" in i and coins==0:
                insArray.append(":".join((i.split(":"))[:2]))
                coins+=1
                couots=0
            elif "out" in i and couots==0:
                outsArray.append(":".join((i.split(":"))[:2]))
                couots+=1
                coins=0
        if punches.index(i)>0 and int((punches[punches.index(i)-1]).split(":")[0]) <= int(i.split(":")[0])and int((punches[punches.index(i)-1]).split(":")[1]) <= int(i.split(":")[1]):
            if "in" in i and coins==0:
                insArray.append(":".join((i.split(":"))[:2]))
                coins+=1
                couots=0
            elif "in" in i and coins>0:
                insArray.append(":".join((i.split(":"))[:2]))
                fidate= (datetime.strptime((":".join(((punches[punches.index(i)-1]).split(":"))[:2])), "%H:%M"))
                fidate1= (datetime.strptime((":".join((i.split(":"))[:2])), "%H:%M"))
                gaptim= (str(fidate1 - fidate)).split(":")
                gapinmins=int(gaptim[0])*60 + int(gaptim[1])
                if int(i.split(":")[0])==14 and int(i.split(":")[1])<=10:
                    if gapinmins<=45:
                        outsArray.append(":".join((i.split(":"))[:2]))
                    else:
                        timetoadd = (":".join(((str((fidate1 - timedelta(minutes=45)).time())).split(":"))[:2]))
                        outsArray.append(timetoadd)
                else:
                    if gapinmins<=15:
                        outsArray.append(":".join((i.split(":"))[:2]))
                    else:
                        timetoadd = (":".join(((str((fidate1 - timedelta(minutes=15)).time())).split(":"))[:2]))
                        outsArray.append(timetoadd)
            elif "out" in i and couots==0 and coins==0:
                outsArray.append(":".join((i.split(":"))[:2]))
                insArray.append(":".join((i.split(":"))[:2]))
                couots+=1
                coins=0
            elif "out" in i and couots==0:
                outsArray.append(":".join((i.split(":"))[:2]))
                couots+=1
                coins=0
            elif "out" in i and couots>0:
                outsArray.append(":".join((i.split(":"))[:2]))
                fidateot= (datetime.strptime((":".join(((punches[punches.index(i)-1]).split(":"))[:2])), "%H:%M"))
                fidateot1= (datetime.strptime((":".join((i.split(":"))[:2])), "%H:%M"))
                gaptim= (str(fidateot1 - fidateot)).split(":")
                gapinmins=int(gaptim[0])*60 + int(gaptim[1])
                if int(i.split(":")[0])==13:
                    if gapinmins<=45:
                        insArray.append(":".join((i.split(":"))[:2]))
                    else:
                        timetoadd = (":".join(((str((fidateot + timedelta(minutes=45)).time())).split(":"))[:2]))
                        insArray.append(timetoadd)
                else:
                    if gapinmins<=15:
                        insArray.append(":".join((i.split(":"))[:2]))
                    else:
                        timetoadd = (":".join(((str((fidateot + timedelta(minutes=15)).time())).split(":"))[:2]))
                        insArray.append(timetoadd)
            
    if len(insArray) > len(outsArray):
        outsArray.append(insArray[len(insArray)-1])
    if len(insArray) < len(outsArray):
        insArray.append(outsArray[len(outsArray)-1])

    for j in range(len(insArray)):
        attendance_dates.append(attendancedate)
        employee_id.append(employeeid)
        attendance_log_id.append(attendancelogid)
        
    punch_in_times = insArray
    punch_out_times = outsArray

    # Create pandas DataFrame
    punch_df = pd.DataFrame({'employee_id': employee_id, 'attendance_log_id': attendance_log_id, 'attendance_date': attendance_dates, 'punch_in': ["" if x == '' else x for x in punch_in_times], 'punch_out': ["" if x == '' else x for x in punch_out_times]})


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
engine = create_engine('mysql+pymysql://root:root@localhost/sys')

# Define MySQL query
query = "SELECT employee_id, attendance_log_id, attendance_date, punch_records FROM stg_attendancelogs where attendance_log_id NOT IN (SELECT attendance_log_id FROM dim_attendance_time)"

# Execute MySQL query and read results into pandas DataFrame
df = pd.read_sql_query(query, engine)

# Create empty lists for punch in and out times and attendance dates


allPunches=[]
allDates=[]
allEmployes=[]
allattendancelogs = []


for punchrecs in df['punch_records']:
    allPunches.append(punchrecs)
for attendanceDate in df['attendance_date']:
    allDates.append(attendanceDate)
for employeeId in df['employee_id']:
    allEmployes.append(employeeId)
for attendancelogid in df['attendance_log_id']:
    allattendancelogs.append(attendancelogid)
allData=[]

for i in range(len(allPunches)):
    if allPunches[i]!="":
        allData.append([allPunches[i], allDates[i], allEmployes[i],allattendancelogs[i]])
        
data = {'employee_id':  [""],
        'attendance_log_id': [""],
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
    cursor.execute("INSERT INTO dim_attendance_time (employee_id, attendance_log_id, attendance_date, punch_in, punch_out) VALUES (%s, %s, %s, %s, %s)", (row['employee_id'], row['attendance_log_id'], row['attendance_date'], row['punch_in'], row['punch_out']))
db.commit()
db.close()