import psycopg2

conn = psycopg2.connect( host="localhost", database="pracuj_pl", user="python_user", password="1234")
		
# create a cursor
cur = conn.cursor()

# query data with cursor for selectin
query = "SELECT * from data_warsaw_all where date_trunc('day', added_at) = '2022-12-02'"
output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

# saving data as CSV
with open('export.csv', 'w', encoding="utf-8") as f:
    cur.copy_expert(output, f)

# close cursor  
conn.close()