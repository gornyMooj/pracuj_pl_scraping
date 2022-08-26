'''
INSERT if does not exist already
'''
import psycopg2

conn = psycopg2.connect( host="localhost", database="pracuj_pl", user="python_user", password="1234")
		
# create a cursor
cur = conn.cursor()


sql = f"""
    INSERT INTO vendors(vendor_name) 
    SELECT '{'wrona'}' 
    WHERE NOT EXISTS (SELECT 1 FROM vendors WHERE vendor_name='{'wrona'}');
"""

# insert data with cursor
cur.execute(sql)

# close cursor
cur.close()
# commit the changes
conn.commit()
# close conection
conn.close()	

