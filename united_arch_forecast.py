import forecast.forecast as fc
import sqlite3
import datetime
from pprint import pprint
import os
import json
import dateutil.parser as p
from datetime import datetime

db_path = "./db.sqlite"
dirpath = "./SWAT_united_test"
city_translit = "./city_translit.json"

def main(stations='all'):
	con = sqlite3.connect(db_path)
	cursor = con.cursor()
	# # check is directory empty
	stations = fc.create_stations()#pass stations here
	stations = fc.perform_calcs(stations)
	files = write_headers(stations, dirpath)
	stations_names = [st.name for st in stations]
	# pprint(stations_names)
	# pprint(files)
	translit = json.load(open(city_translit, mode='r'))
	write_pcp_from_db(files['pcp_file'], cursor, translit, stations_names)


def write_pcp_from_db(pcp_file, cursor, translit, stations_names):
	pcp_data = get_data_from_db(cursor, translit, stations_names)
	file = open(pcp_file, mode='a')
	i = 0
	days_count = len(pcp_data[0]['data'])
	while i < days_count:
		date = p.parse(pcp_data[0]['data'][i][0])
		year = date.year
		first_jan = datetime(int(date.year), 1, 1)
		delta = date - first_jan
		# file.write("{}{:03}".format(year, delta.days + 1))
		for st in pcp_data:
			try:
				day_pcp = st['data'][i][1]
			except IndexError:
				print(st['name'])
				print(i)
			# print(st['name'])
			if day_pcp == None:
				day_pcp = 0.0
			# file.write("{:05.1f}".format(day_pcp))
		# print('i=', i)
		i += 1
		file.write('\n')

def get_data_from_db(cursor, translit, stations_names):
	data = []
	for st_name in stations_names:
		translited_name = translit[st_name]
		st_data = {}
		st_data['name'] = st_name
		st_data['alter_name'] = translited_name
		st_records = cursor.execute("""
			SELECT dt, pcp from {} ORDER BY dt
			""".format(translited_name)).fetchall()
		st_data['data'] = st_records
		data.append(st_data)
	return data

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