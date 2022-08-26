'''
SOURCE: https://www.postgresqltutorial.com/postgresql-python/insert/
- INSERT DATA
'''


import psycopg2

conn = psycopg2.connect( host="localhost", database="pracuj_pl", user="python_user", password="1234")
		
# create a cursor
cur = conn.cursor()


sql = "INSERT INTO vendors(vendor_name) VALUES(%s)"

# insert data with cursor
cur.execute(sql, [('Belucio Inc.',)])
# THIS CAN BE USED FOR INSERTING A LIST: cur.executemany(sql,vendor_list)

# close cursor
cur.close()
# commit the changes
conn.commit()
# close conection
conn.close()	


