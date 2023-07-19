import pandas as pd
import pyodbc

# Define the connection string for the Access database
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\Users\ShubhamDilipVhanmane\Desktop\ESSL\eTimeTrackLite_2023_04_21_1.mdb;'
)

# Create the pyodbc connection using the connection string
conn = pyodbc.connect(conn_str)

# Define the SQL query to retrieve data from the Access database
sql_query = 'SELECT * FROM Devices;'

# Load the data into a Pandas dataframe using the pyodbc connection
df = pd.read_sql_query(sql_query, conn)

# Define the connection string for the MySQL database
mysql_conn_str = 'mysql+mysqlconnector://root:root@localhost/sys'

# Create the SQLAlchemy engine using the MySQL connection string
mysql_engine = create_engine(mysql_conn_str)

# Insert the data into the MySQL database using the SQLAlchemy engine
df.to_sql('Devices', mysql_engine, if_exists='replace', index=False)

# Close the connections
conn.close()
mysql_engine.dispose()