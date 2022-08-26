'''
SOURCE: https://www.postgresqltutorial.com/postgresql-python/insert/
- Querying Data

options when fetching data:
    ->  fetchone(),  fetchall(), or  fetchmany()
'''


import psycopg2

conn = psycopg2.connect( host="localhost", database="pracuj_pl", user="python_user", password="1234")
		
# create a cursor
cur = conn.cursor()



# query data with cursor
cur.execute("SELECT vendor_id, vendor_name, added_at FROM vendors ORDER BY vendor_name")
rows = cur.fetchall()

# close cursor
cur.close()
# commit the changes
conn.commit()
# close conection
conn.close()	

for row in rows:
    print(row)