import sys
import datetime as dt
import sqlite3
from pprint import pprint

conn = sqlite3.connect("./db.sqlite")
cursor = conn.cursor()

tables = cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table';
    """).fetchall()
tables = [el[0] for el in tables]

for table in tables:
	res = cursor.execute('''
		DELETE FROM {}
		where dt >= '2019-02-01'
		'''.format(table)).fetchall()
	print(res)
conn.commit()
conn.close()