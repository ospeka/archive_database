import sqlite3
from pprint import pprint

conn = sqlite3.connect("./db.sqlite")
cursor = conn.cursor()

tables = cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table';
    """).fetchall()
tables = [el[0] for el in tables]

pprint(tables)

for table in tables:
	res = cursor.execute("""
		SELECT id,dt FROM {}
		WHERE t='' or tmin='' or tmax=''
		""".format(table)).fetchall()
	print(res)
