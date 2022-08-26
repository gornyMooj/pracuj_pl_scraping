'''
pracuj_pl data schema
opens csv reads column names 
adds data to the table

'''
import pandas as pd
import psycopg2

# generate a table schema based on the CSV with the scraped data
df = pd.read_csv('./PostgreSQL/sample_pracuj_pl_data.csv')

row = df.loc[8, :].values.tolist()
row = [ str(i).strip() for i in row]

col_names = list(df.columns)
col_names_db = [col_name.replace("-", "_") for col_name in col_names]


base = ""
for i,v in enumerate(col_names_db):
    base = base + " " + str(v) + "='" + str(row[i]) + "'"
    if i + 1 != len(col_names_db):
        base += " AND"

SQL = f"""INSERT INTO data_warsaw({' ,'.join(col_names_db)})
        SELECT {" ,".join([ "'" + str(v) + "'" for v in row])}
        WHERE NOT EXISTS (SELECT 1 FROM data_warsaw WHERE {base});"""

print()
print(SQL)
print()


conn = psycopg2.connect( host="localhost", database="pracuj_pl", user="python_user", password="1234")
		
# create a cursor
cur = conn.cursor()

# insert data with cursor
cur.execute(SQL)

# close cursor
cur.close()
# commit the changes
conn.commit()
# close conection
conn.close()

print('Done')















