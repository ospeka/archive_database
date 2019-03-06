import sqlite3
import os
from pprint import pprint
import csv
from datetime import datetime
import dateutil.parser as dt_parser

csvs_dir = "./desna_ua_meteo_for_db"

def main():
	conn = sqlite3.connect("./db.sqlite")
	cursor = conn.cursor()
	files = os.listdir(csvs_dir)
	# for file in files:
	# 	refill_table(file, cursor)
	dt = datetime(year=2000, month=1, day=5)
	resp = cursor.execute("""
		SELECT dt, pcp FROM Chernigiv
		WHERE dt >= (?)
		""", (dt,)).fetchall()
	pprint(resp[:10])

	conn.commit()
	conn.close()


def refill_table(file, cursor):
	reader = csv.reader(open(csvs_dir + '/' + file))
	data = [el for el in reader]
	table_name = file.split('.')[0]
	print(table_name)
	# clear table
	cursor.execute("""
		DELETE FROM {}
		""".format(table_name))
	# insert new data. id - autoincrement
	for line in data[1:]:
		line[0] = None
		line[1] = dt_parser.parse(line[1])
		cursor.execute(
			"""
			INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?)
			""".format(table_name), tuple(line)
			)
	print(data[0])
	print(data[1])


if __name__ == '__main__':
	main()