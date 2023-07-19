import socket
import tqdm
import os
import time

import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import time

# IP OF RECIVER 
SERVER_HOST = "0.0.0.0"
# RUN PORT
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>" 

# MENTIONING SOCKET AND ASSIGNING TO VARIABLE
s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))  # BINDING THE IP AND THE HOST

while True:
    # LISTING TO THE CLIENT 
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    # CONNECTING TO THE CLIENT IP AND GETTING THE FILE
    client_socket, address = s.accept()
    print(f"[+] {address} is connected.")

    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)

    # GETTING THE FILE SIZE
    filesize = int(filesize)
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'  
        r'DBQ="C:\Users\ShubhamDilipVhanmane\Desktop\cloud angles\ESSL Time tracking soft\raw\eTimeTrackLite_2023_04_17_1.mdb";'
        )
    
    conn = pyodbc.connect(conn_str)
    sql_query = 'SELECT * FROM Employees;'
    df = pd.read_sql_query(sql_query, conn)
    sql_query = 'SELECT * FROM AttendanceLogs;'
    df = pd.read_sql_query(sql_query, conn)
    mysql_conn_str = 'mysql+mysqlconnector://root:root@localhost/sys'
    mysql_engine = create_engine(mysql_conn_str)
    df.to_sql('Employees', mysql_engine, if_exists='replace', index=False)
    df.to_sql('AttendanceLogs', mysql_engine, if_exists='replace', index=False)

    conn.close()
    mysql_engine.dispose()
    # client_socket.close()
    # s.close()



    