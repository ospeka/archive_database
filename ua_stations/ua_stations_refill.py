import sqlite3
import os
from pprint import pprint
import csv
from datetime import datetime
import dateutil.parser as dt_parser

csvs_dir = "./desna_ua_meteo_for_db"
db_path = "../db.sqlite"

def main():
	conn = sqlite3.connect(db_path)
	cursor = conn.cursor()
	files = os.listdir(csvs_dir)
	for file in files:
		refill_table(file, cursor)
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
		try:
			line[-1] = round(float(line[-1]) / 100, 3)
		except ValueError:
			line[-1] = None
		cursor.execute(
			"""
			INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?)
			""".format(table_name), tuple(line)
			)


if __name__ == '__main__':
	main()