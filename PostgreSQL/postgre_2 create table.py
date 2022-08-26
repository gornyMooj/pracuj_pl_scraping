'''
- Exmaple taken from: https://www.postgresqltutorial.com/postgresql-python/create-tables/
- CREATE TABLE
'''

import psycopg2

conn = psycopg2.connect( host="localhost", database="pracuj_pl",  user="python_user", password="1234")
		
# create a cursor
cur = conn.cursor()

command = """
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL,
            added_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
        """

# create a table with cursor
cur.execute(command)

# close cursor
cur.close()
# commit the changes
conn.commit()
print('Table created...')
# close conection
conn.close()	
