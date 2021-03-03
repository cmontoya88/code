import pandas as pd
import pyodbc

cnx = pyodbc.connect('Driver={SQL Server};Server=MyServer;Database=MyDatabase;UID=Username;PWD=Password;Trusted_Connection=yes;')

# Query
query = 'SELECT * FROM [Datasets].[dbo].[dataset]'

# Print to data in Table DB
cursor = cnx.cursor()
cursor.execute(query)
for row in cursor:
    print(row)

# Generate files from Dataset
sql_query = pd.read_sql_query(query, cnx)
df = pd.DataFrame(sql_query)
df.to_excel(r'D:\export_dataset_test.xlsx', index=False, header=True)
