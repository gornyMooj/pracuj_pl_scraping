'''
pracuj_pl data schema
opens csv reads column names 
creates the SQL command for the table creation
create table in the database
'''
import pandas as pd
import psycopg2

# generate a table schema based on the CSV with the scraped data
df = pd.read_csv('./PostgreSQL/sample_pracuj_pl_data.csv')

col_names = list(df.columns)

SQL = """CREATE TABLE data_warsaw_all (
            work_id SERIAL PRIMARY KEY,
            added_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),"""

for col_name in col_names:
    col_name = col_name.replace("-", "_")
    SQL += f"""
    {col_name} VARCHAR(800),"""
    if col_name == col_names[-1]: 
        SQL = SQL[:-1] + """
        )"""

print("Generated SQL QUERY:\n")
print(SQL)




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







