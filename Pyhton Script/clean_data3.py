import mysql.connector
import pandas as pd
import datetime
from datetime import timedelta
from sqlalchemy import create_engine

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
query = "SELECT employee_id, attendance_log_id, attendance_date, punch_in, punch_out FROM dim_attendance_time where attendance_log_id NOT IN (SELECT attendance_log_id FROM dim_attendance_break_time)"

# Execute MySQL query and read results into pandas DataFrame
df = pd.read_sql_query(query, engine)

allEmployeeIds=sorted(list(set(list(df['employee_id']))))
allattendancelogid=sorted(list(set(list(df['attendance_log_id']))))
allDates=sorted(list(set(list(df['attendance_date']))))


alltimediff=[]
alldates=[]
allemployeeIds=[]
allattendancelogid = []

for i in allEmployeeIds:
    for j in allDates:
        timelist = []
        querydy = "SELECT employee_id, attendance_log_id, attendance_date, punch_in, punch_out FROM dim_attendance_time WHERE attendance_log_id NOT IN (SELECT attendance_log_id FROM dim_attendance_break_time) and employee_id = {} and attendance_date = '{}'".format(i, j)
        dataofempday=pd.read_sql_query(querydy, engine)
#         print(dataofempday)
        punchin=list(dataofempday.punch_in)
        punchout=list(dataofempday.punch_out)
        for k in range(len(punchin)-1):
            diftime = punchin[k+1]-punchout[k]
            totaltime=int(((str(diftime).split(" ")[2]).split(":"))[0])*60 + int(((str(diftime).split(" ")[2]).split(":"))[1])
            timelist.append(totaltime)
#         print(timelist)
        # print(timedelta(minutes=sum(timelist)))
        alltimediff.append(sum(timelist))
        alldates.append(j)
        allemployeeIds.append(i)
            
data = {'employee_id':  allemployeeIds,
        'attendance_date': alldates,
        'break_in_minutes': alltimediff
        }

allBreakMinutes=pd.DataFrame(data)

# Convert break time to minutes
# alldatamerged = df['break_time'].dt.total_seconds() / 60

# print(allBreakMinutes.iloc[3: 350])
# print(allBreakMinutes.head(50))
# cursor = db.cursor()
# for i, row in allBreakMinutes.iterrows():
#     cursor.execute("INSERT INTO dim_attendance_break_time (employee_id, attendance_date, break_in_minutes) VALUES (%s, %s, %s)", (row['employee_id'], row['attendance_date'], row['break_in_minutes']))
# db.commit()
# db.close()

