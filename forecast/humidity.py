from .pcp import num_of_records_by_day
from datetime import datetime
import os

def write_hmd(stations, dirpath):
	if (os.sep != '/'):
		dirpath = dirpath.replace('/', os.sep)
	file = open(os.path.join(dirpath, "hmd.hmd"), "w+")
	file.write("Input File hmd.hmd          3/2/2018 ArcSWAT 2012.10_4.19\n")
	days = stations[0].pcp.keys()
	for day in days:
		file.write(str(day.year))
		first_jan = datetime(int(day.year), 1 ,1)
		delta = day - first_jan
		file.write("{:03}".format(delta.days))
		for st in stations:
			file.write("{:08.3f}".format(st.hmd[day]))
		file.write('\n')

def calc_hmd(station):
	num_of_recs = num_of_records_by_day(station.data)
	days = num_of_recs.keys()
	i = 0
	for day in days:
		if (num_of_recs[day] != 8):
			i += num_of_recs[day]
		else:
			station.hmd[day] = count_hmd(station.data,i)
			i += 8
	return (station.hmd)

def count_hmd(data, i):
	part = data[i:i+8]
	summmary = 0
	for rec in part:
		summmary += rec["main"]["humidity"]
	summmary = round(summmary / 8, 3)
	return(summmary)
