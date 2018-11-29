from .pcp import num_of_records_by_day
from datetime import datetime, timedelta, timezone
import os

def write_wind(stations, dirpath):
	if (os.sep != '/'):
		dirpath = dirpath.replace('/', os.sep)
	file = open(os.path.join(dirpath, "wnd.wnd"), "w+")
	file.write("Input File wnd.wnd          3/2/2018 ArcSWAT 2012.10_4.19\n")
	days = stations[0].pcp.keys()
	for day in days:
		file.write(str(day.year))
		first_jan = datetime(int(day.year), 1 ,1)
		delta = day - first_jan
		file.write("{:03}".format(delta.days))
		for st in stations:
			file.write("{:08.3f}".format(st.wind[day]))
		file.write('\n')

def calc_wind(station):
	num_of_recs = num_of_records_by_day(station.data)
	days = num_of_recs.keys()
	i = 0
	for day in days:
		if (num_of_recs[day] != 8):
			i += num_of_recs[day]
		else:
			station.wind[day] = count_wind(station.data,i)
			i += 8
	return (station.wind)

def count_wind(data, i):
	part = data[i:i+8]
	summmary = 0
	for rec in part:
		summmary += rec["wind"]["speed"]
	summmary = round(summmary / 8, 3)
	return(summmary)
