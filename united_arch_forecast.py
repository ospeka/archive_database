import forecast.forecast as fc
import sqlite3
from datetime import datetime
from pprint import pprint
import os

db_path = "./db.sqlite"
dirpath = "./SWAT_united_test"

def main():
	con = sqlite3.connect(db_path)
	cursor = con.cursor()
	# pcp = cursor.execute("""
	# 	SELECT dt, pcp FROM Bryansk ORDER BY dt
	# """).fetchall()
	# # dt_object = datetime.fromisoformat(pcp1[0])
	# pcp_dt_objects = []
	# for el in pcp:
	# 	pcp_record = {}
	# 	pcp_record['date'] = datetime.fromisoformat(el[0])
	# 	if el[1]:
	# 		pcp_record['pcp'] = el[1]
	# 	else:
	# 		pcp_record['pcp'] = 0
	# 	pcp_dt_objects.append(pcp_record)
	# for el in pcp_dt_objects:
	# 	day = el['date']
	# 	first_jan = datetime(day.year, 1, 1)
	# 	print(day.year, end='')
	# 	delta = day - first_jan
	# 	days = int(delta.days) + 1
	# 	# print(days, end='')
	# 	print("{:03d}".format(days), end='')
	# 	print("{:05.1f}".format(el['pcp']), end='')
	# 	print()

	# directory = './'
	# # check is directory empty
	# paths = write_headers(directory)
	# from_db = get_data_from_db(cursor)
	# print('city name - ', from_db[0]['city'])
	# test_data = from_db[0]['data'][:10]
	# pprint(test_data)

	# stations = fc.create_stations()
	# stations = fc.perform_calcs(stations)
	# files = write_headers(stations, dirpath)
	# write_pcp_from_db(files['pcp_file'], cursor)
	# print(files)
	res = cursor.execute("""
		SELECT name FROM sqlite_master WHERE type='table';
	""").fetchall()
	res = [el[0] for el in res]
	pprint(res)

def write_pcp_from_db(pcp_file, cursor):
	pass

def write_headers(stations, dirpath):
	pcp_file = write_pcp_header(stations, dirpath)
	clouds_file = write_clouds_header(stations, dirpath)
	hum_file = write_hum_header(stations, dirpath)
	temp_file = write_temp_header(stations, dirpath)
	wind_file = write_wind_header(stations, dirpath)
	return {'pcp_file': pcp_file,
			'clouds_file': clouds_file,
			'hum_file': hum_file,
			'temp_file': temp_file,
			'wind_file': wind_file}

def write_pcp_header(stations, dirpath):
	if os.sep != '/':
		dirpath = dirpath.replace('/', os.sep)
	file = open(os.path.join(dirpath, "pcp.pcp"), "w+")
	file.write("Stations  ")
	for st in stations:
		file.write(st.name + "_PCP,")
	file.write('\n')
	file.write("Lati    ")
	for st in stations:
		file.write(str(st.lat) + ' ')
	file.write('\n')
	file.write("Long    ")
	for st in stations:
		file.write(str(st.lon) + ' ')
	file.write('\n')
	file.write("Elev     ")
	for st in stations:
		file.write(str(st.elev) + "  ")
	file.write('\n')
	file.close()
	return os.path.join(dirpath, "pcp.pcp")

def write_clouds_header(stations, dirpath):
	if (os.sep != '/'):
		dirpath = dirpath.replace('/', os.sep)
	file = open(os.path.join(dirpath, "slr.slr"), "w+")
	file.write("Input File slr.slr          3/2/2018 ArcSWAT 2012.10_4.19\n")
	return os.path.join(dirpath, "slr.slr")

def write_hum_header(stations, dirpath):
	if (os.sep != '/'):
		dirpath = dirpath.replace('/', os.sep)
	file = open(os.path.join(dirpath, "hmd.hmd"), "w+")
	file.write("Input File hmd.hmd          3/2/2018 ArcSWAT 2012.10_4.19\n")
	file.close()
	return os.path.join(dirpath, "hmd.hmd")

def write_temp_header(stations, dirpath):
	if (os.sep != '/'):
		dirpath = dirpath.replace('/', os.sep)
	file = open(os.path.join(dirpath, "Tmp.tmp"), "w+")
	file.write("Stations  ")
	for st in stations:
		file.write(st.name + "_TMP,")
	file.write('\n')
	file.write("Lati    ")
	for st in stations:
		file.write(str(st.lat)  + ' ')
	file.write('\n')
	file.write("Long    ")
	for st in stations:
		file.write(str(st.lon) + ' ')
	file.write('\n')
	file.write("Elev     ")
	for st in stations:
		file.write(str(st.elev) + "  ")
	file.write('\n')
	file.close()
	return os.path.join(dirpath, "Tmp.tmp")

def write_wind_header(stations, dirpath):
	if (os.sep != '/'):
		dirpath = dirpath.replace('/', os.sep)
	file = open(os.path.join(dirpath, "wnd.wnd"), "w+")
	file.write("Input File wnd.wnd          3/2/2018 ArcSWAT 2012.10_4.19\n")
	return os.path.join(dirpath, "wnd.wnd")

if __name__ == '__main__':
    main()