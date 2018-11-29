from datetime import datetime, timedelta
import os


def count_pcp(station):
	num_records = num_of_records_by_day(station.data)
	i = 0
	pcp = {}
	for key in num_records.keys():
		if num_records[key] != 8:
			i += num_records[key]
		else:
			sum_by_day = count_sum(i, station.data)
			pcp[key] = round(sum_by_day, 1)
			i += 8
	return pcp


def count_sum(i, records):
	needed_records = records[i:i+8]
	summary = 0
	for rec in needed_records:
		if "rain" in rec.keys() and rec["rain"] != {}:
			summary += rec["rain"]["3h"]
	return summary


def num_of_records_by_day(records):
	num_records = {}
	for record in records:
		dt1 = datetime.fromtimestamp(record["dt"])
		dt1 = dt1.replace(hour=0)
		num_records[dt1] = 0
		for record2 in records:
			dt2 = datetime.fromtimestamp(record2["dt"])
			if dt1.year == dt2.year and dt1.month == dt2.month and dt1.day == dt2.day:
				num_records[dt1] += 1
	return num_records


def write_pcp(stations, dirpath):
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
	days = stations[0].pcp.keys()
	for day in days:
		file.write(str(day.year))
		first_jan = datetime(int(day.year), 1, 1)
		delta = day - first_jan
		file.write("{:03}".format(delta.days))
		for st in stations:
			file.write("{:05.1f}".format(st.pcp[day]))
		file.write('\n')
