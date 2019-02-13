from .pcp import num_of_records_by_day
import csv
from datetime import datetime
import os

irrad_file = './forecast/Солнечная_радиация_станд_значения.csv'
a = 0.4
b = 0.38


def write_clouds(stations, dirpath):
    if (os.sep != '/'):
        dirpath = dirpath.replace('/', os.sep)
    file = open(os.path.join(dirpath, "slr.slr"), "w+")
    file.write("Input File slr.slr          3/2/2018 ArcSWAT 2012.10_4.19\n")
    days = stations[0].pcp.keys()
    for day in days:
        file.write(str(day.year))
        first_jan = datetime(int(day.year), 1, 1)
        delta = day - first_jan
        file.write("{:03}".format(delta.days))
        for st in stations:
            file.write("{:08.3f}".format(st.clouds[day]))
        file.write('\n')


def calc_clouds(station):
    num_of_recs = num_of_records_by_day(station.data)
    days = num_of_recs.keys()
    i = 0
    for day in days:
        if (num_of_recs[day] != 8):
            i += num_of_recs[day]
        else:
            station.clouds[day] = count_clouds(station.data, i)
            i += 8
    use_formula(station)
    return (station.clouds)


def use_formula(station):
    data = []
    with open(irrad_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        data = [line for line in reader]
    city_index = data[0].index(station.name)
    for day in station.clouds.keys():
        q_zero = float(data[day.month][city_index])
        n = station.clouds[day]
        station.clouds[day] = round(q_zero * (1 - (a + b * n) * n), 3)


def count_clouds(data, i):
    part = data[i:i + 8]
    summmary = 0
    for rec in part:
        summmary += rec["clouds"]["all"]
    summmary = summmary / 800
    return(summmary)
