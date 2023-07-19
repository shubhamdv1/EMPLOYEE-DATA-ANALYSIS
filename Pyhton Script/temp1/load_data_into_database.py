
import pandas as pd
import pyodbc
from sqlalchemy import create_engine


# Define the connection string for the Access database
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\ShubhamDilipVhanmane\Desktop\ESSL\eTimeTrackLite_2023_04_17_1.mdb;'
)

# Create the pyodbc connection using the connection string
conn = pyodbc.connect(conn_str)

# Define the SQL query to retrieve data from the Access database
sql_query = 'SELECT * FROM employees;'

# Define the SQL query to retrieve data from the Access database
sql_query1 = 'SELECT * FROM attendancelogs;'

# Load the data into a Pandas dataframe using the pyodbc connection
df = pd.read_sql_query(sql_query, conn)

# Load the data into a Pandas dataframe using the pyodbc connection
df1 = pd.read_sql_query(sql_query1, conn)

# Define the connection string for the MySQL database
mysql_conn_str = 'mysql+mysqlconnector://root:root@localhost/essl'

# Create the SQLAlchemy engine using the MySQL connection string
mysql_engine = create_engine(mysql_conn_str)

# Insert the data into the MySQL database using the SQLAlchemy engine
df.to_sql('employees', mysql_engine, if_exists='replace', index=False)

# Insert the data into the MySQL database using the SQLAlchemy engine
df1.to_sql('attendancelogs', mysql_engine, if_exists='replace', index=False)

# Close the connections
conn.close()
mysql_engine.dispose()

