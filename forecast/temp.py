from datetime import datetime
from .pcp import num_of_records_by_day
import os

temp_min_kelv = -273.15


def calc_temp(station):
    num_of_recs = num_of_records_by_day(station.data)
    days = num_of_recs.keys()
    i = 0
    for day in days:
        if (num_of_recs[day] != 8):
            i += num_of_recs[day]
        else:
            min_temp, max_temp = find_min_max(station.data, i)
            station.temp[day] = {}
            station.temp[day]["min_temp"] = round(min_temp + temp_min_kelv, 3)
            station.temp[day]["max_temp"] = round(max_temp + temp_min_kelv, 3)
            i += 8
    return (station.temp)


def find_min_max(data, i):
    part = data[i:i + 8]
    min_temp = part[0]["main"]["temp"]
    max_temp = part[0]["main"]["temp"]
    for record in part:
        if (record["main"]["temp"] < min_temp):
            min_temp = record["main"]["temp"]
        if (record["main"]["temp"] > max_temp):
            max_temp = record["main"]["temp"]
    return (min_temp, max_temp)


def write_temp(stations, dirpath):
    if (os.sep != '/'):
        dirpath = dirpath.replace('/', os.sep)
    file = open(os.path.join(dirpath, "Tmp.tmp"), "w+")
    file.write("Stations  ")
    for st in stations:
        file.write(st.name + "_TMP,")
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
            file.write("{:-05.1f}".format(st.temp[day]["max_temp"]))
            file.write("{:-05.1f}".format(st.temp[day]["min_temp"]))
        file.write('\n')
