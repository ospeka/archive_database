# This file get data from db via db_path
# creting swat files in dir defined in dirpath
# write swat file headers from data in st_data.json file
# table names doesnt match with station names so
# its city_transli.json file
# then it performs calcs and write data in swat format

import sqlite3
import os
import json
import dateutil.parser as dt_parser
from datetime import datetime
import csv

db_path = "../db.sqlite"
dirpath = "./SWAT_united_test"
st_data_path = "../st_data.json"
city_translit = "../city_translit.json"
irrad_file = "../forecast/Солнечная_радиация_станд_значения.csv"
a = 0.4
b = 0.38
Cor_factor = 0.4
start_date = datetime(year=2011, month=1, day=1)
end_date = datetime.now().date()


def write_swat_from_db(dirpath):
    # update db before run this file!!!
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    st_data = json.load(open(st_data_path, mode='r'))
    # stations = fc.create_stations()
    # stations = fc.perform_calcs(stations)

    files = write_headers(st_data, dirpath)
    stations_names = [st["name"] for st in st_data]
    translit = json.load(open(city_translit, mode='r'))
    write_pcp_from_db(files['pcp_file'], cursor, translit, stations_names)
    write_temp_from_db(files['temp_file'], cursor, translit, stations_names)
    write_wind_from_db(files['wind_file'], cursor, translit, stations_names)
    write_hum_from_db(files['hum_file'], cursor, translit, stations_names)
    write_slrdata_from_db(files['clouds_file'], cursor, translit, stations_names)


def write_slrdata_from_db(slr_file, cursor, translit, stations_names):
    clouds_data = get_clouds_data_from_db(cursor, translit, stations_names)
    file = open(slr_file, mode='a')
    with open(irrad_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        irr_data = [line for line in reader]
    i = 0
    days_count = len(clouds_data[0]['data'])
    while i < days_count:
        date = dt_parser.parse(clouds_data[0]['data'][i][0])
        year = date.year
        first_jan = datetime(int(date.year), 1, 1)
        delta = date - first_jan
        file.write("{}{:03}".format(year, delta.days + 1))
        for st in clouds_data:
            try:
                clouds = st['data'][i][1]
                # recount to solar radiation here
                slr = use_formula(clouds, irr_data, date, st['name'])
            except IndexError:
                print(st['name'])
                print(i)
            try:
                file.write("{:08.3f}".format(slr))
            except TypeError:
                print(st['name'], date, clouds, slr)
        i += 1
        file.write("\n")


def use_formula(clouds, irr_data, date, st_name):
    st_index = irr_data[0].index(st_name)
    month_index = date.month
    q_zero = float(irr_data[month_index][st_index])
    n = clouds / 10
    slr = q_zero * (1 - (a + b * n) * n)
    slr *= (1 + Cor_factor)
    return round(slr, 3)


def get_clouds_data_from_db(cursor, translit, stations_names):
    data = []
    for st_name in stations_names:
        translited_name = translit[st_name]
        st_data = {}
        st_data['name'] = st_name
        st_data['alter_name'] = translited_name
        st_records = cursor.execute("""
            SELECT dt, cloud from {}
            WHERE dt >= (?) and dt < (?)
            ORDER BY dt
            """.format(translited_name), (str(start_date), str(end_date))).fetchall()
        st_data['data'] = st_records
        data.append(st_data)
    return data


def write_hum_from_db(hum_file, cursor, translit, stations_names):
    hum_data = get_humdata_from_db(cursor, translit, stations_names)
    file = open(hum_file, mode='a')
    i = 0
    days_count = len(hum_data[0]['data'])
    while i < days_count:
        date = dt_parser.parse(hum_data[0]['data'][i][0])
        year = date.year
        first_jan = datetime(int(date.year), 1, 1)
        delta = date - first_jan
        file.write("{}{:03}".format(year, delta.days + 1))
        for st in hum_data:
            try:
                hum = st['data'][i][1]
            except IndexError:
                print(st['name'])
                print(i)
            try:
                file.write("{:08.3f}".format(hum))
            except TypeError:
                print(st['name'], date, hum)
        i += 1
        file.write("\n")


def get_humdata_from_db(cursor, translit, stations_names):
    data = []
    for st_name in stations_names:
        translited_name = translit[st_name]
        st_data = {}
        st_data['name'] = st_name
        st_data['alter_name'] = translited_name
        st_records = cursor.execute("""
            SELECT dt, hum from {}
            WHERE dt >= (?) and dt < (?)
            ORDER BY dt
            """.format(translited_name), (str(start_date), str(end_date))).fetchall()
        st_data['data'] = st_records
        data.append(st_data)
    return data


def write_wind_from_db(wind_file, cursor, translit, stations_names):
    wind_data = get_winddata_from_db(cursor, translit, stations_names)
    file = open(wind_file, mode='a')
    i = 0
    days_count = len(wind_data[0]['data'])
    while i < days_count:
        date = dt_parser.parse(wind_data[0]['data'][i][0])
        year = date.year
        first_jan = datetime(int(date.year), 1, 1)
        delta = date - first_jan
        file.write("{}{:03}".format(year, delta.days + 1))
        for st in wind_data:
            try:
                wind = st['data'][i][1]
            except IndexError:
                print(st['name'])
                print(i)
            try:
                file.write("{:08.3f}".format(wind))
            except TypeError:
                print(st['name'], date, wind)
        i += 1
        file.write("\n")


def get_winddata_from_db(cursor, translit, stations_names):
    data = []
    for st_name in stations_names:
        translited_name = translit[st_name]
        st_data = {}
        st_data['name'] = st_name
        st_data['alter_name'] = translited_name
        st_records = cursor.execute("""
            SELECT dt, wind from {}
            WHERE dt >= (?) and dt < (?)
            ORDER BY dt
            """.format(translited_name), (str(start_date), str(end_date))).fetchall()
        st_data['data'] = st_records
        data.append(st_data)
    return data


def write_temp_from_db(temp_file, cursor, translit, stations_names):
    temp_data = get_tempdata_from_db(cursor, translit, stations_names)
    file = open(temp_file, mode='a')
    i = 0
    days_count = len(temp_data[0]['data'])
    while i < days_count:
        date = dt_parser.parse(temp_data[0]['data'][i][0])
        year = date.year
        first_jan = datetime(int(date.year), 1, 1)
        delta = date - first_jan
        file.write("{}{:03}".format(year, delta.days + 1))
        for st in temp_data:
            try:
                max_temp = st['data'][i][1]
                min_temp = st['data'][i][2]
            except IndexError:
                print(st['name'])
                print(i)
            
            file.write("{:-05.1f}".format(float(max_temp)))
            file.write("{:-05.1f}".format(float(min_temp)))
        i += 1
        file.write("\n")


def get_tempdata_from_db(cursor, translit, stations_names):
    data = []
    for st_name in stations_names:
        translited_name = translit[st_name]
        st_data = {}
        st_data['name'] = st_name
        st_data['alter_name'] = translited_name
        st_records = cursor.execute("""
            SELECT dt, tmax, tmin from {}
            WHERE dt >= (?) and dt < (?)
            ORDER BY dt
            """.format(translited_name), (str(start_date), str(end_date))).fetchall()
        st_data['data'] = st_records
        data.append(st_data)
    return data


def write_pcp_from_db(pcp_file, cursor, translit, stations_names):
    pcp_data = get_pcpdata_from_db(cursor, translit, stations_names)
    file = open(pcp_file, mode='a')
    i = 0
    days_count = len(pcp_data[0]['data'])
    while i < days_count:
        date = dt_parser.parse(pcp_data[0]['data'][i][0])
        year = date.year
        first_jan = datetime(int(date.year), 1, 1)
        delta = date - first_jan
        file.write("{}{:03}".format(year, delta.days + 1))
        for st in pcp_data:
            try:
                day_pcp = st['data'][i][1]
            except IndexError:
                print(st['name'])
                print(i)
            if day_pcp is None or not day_pcp:
                day_pcp = 0.0
            file.write("{:05.1f}".format(float(day_pcp)))
        i += 1
        file.write('\n')


def get_pcpdata_from_db(cursor, translit, stations_names):
    data = []
    for st_name in stations_names:
        translited_name = translit[st_name]
        st_data = {}
        st_data['name'] = st_name
        st_data['alter_name'] = translited_name
        st_records = cursor.execute("""
            SELECT dt, pcp from {}
            WHERE dt >= (?) and dt < (?)
            ORDER BY dt
            """.format(translited_name), (str(start_date), str(end_date))).fetchall()
        st_data['data'] = st_records
        data.append(st_data)
    return data


def write_headers(st_data, dirpath):
    pcp_file = write_pcp_header(st_data, dirpath)
    clouds_file = write_clouds_header(st_data, dirpath)
    hum_file = write_hum_header(st_data, dirpath)
    temp_file = write_temp_header(st_data, dirpath)
    wind_file = write_wind_header(st_data, dirpath)
    return {'pcp_file': pcp_file,
            'clouds_file': clouds_file,
            'hum_file': hum_file,
            'temp_file': temp_file,
            'wind_file': wind_file}


def write_pcp_header(st_data, dirpath):
    if os.sep != '/':
        dirpath = dirpath.replace('/', os.sep)
    file = open(os.path.join(dirpath, "pcp1.pcp"), "w+")
    file.write("Stations  ")
    for st in st_data:
        file.write(st["name"] + "_PCP,")
    file.write('\n')
    file.write("Lati    ")
    for st in st_data:
        file.write(str(st["lat"]) + ' ')
    file.write('\n')
    file.write("Long    ")
    for st in st_data:
        file.write(str(st["lon"]) + ' ')
    file.write('\n')
    file.write("Elev     ")
    for st in st_data:
        file.write(str(st["elev"]) + "  ")
    file.write('\n')
    file.close()
    return os.path.join(dirpath, "pcp1.pcp")


def write_clouds_header(st_data, dirpath):
    if (os.sep != '/'):
        dirpath = dirpath.replace('/', os.sep)
    file = open(os.path.join(dirpath, "slr.slr"), "w+")
    file.write("Input File slr.slr          3/2/2018 ArcSWAT 2012.10_4.19\n")
    return os.path.join(dirpath, "slr.slr")


def write_hum_header(st_data, dirpath):
    if (os.sep != '/'):
        dirpath = dirpath.replace('/', os.sep)
    file = open(os.path.join(dirpath, "hmd.hmd"), "w+")
    file.write("Input File hmd.hmd          3/2/2018 ArcSWAT 2012.10_4.19\n")
    file.close()
    return os.path.join(dirpath, "hmd.hmd")


def write_temp_header(st_data, dirpath):
    if (os.sep != '/'):
        dirpath = dirpath.replace('/', os.sep)
    file = open(os.path.join(dirpath, "Tmp1.tmp"), "w+")
    file.write("Stations  ")
    for st in st_data:
        file.write(st["name"] + "_TMP,")
    file.write('\n')
    file.write("Lati    ")
    for st in st_data:
        file.write(str(st["lat"]) + ' ')
    file.write('\n')
    file.write("Long    ")
    for st in st_data:
        file.write(str(st["lon"]) + ' ')
    file.write('\n')
    file.write("Elev     ")
    for st in st_data:
        file.write(str(st["elev"]) + "  ")
    file.write('\n')
    file.close()
    return os.path.join(dirpath, "Tmp1.tmp")


def write_wind_header(stations, dirpath):
    if (os.sep != '/'):
        dirpath = dirpath.replace('/', os.sep)
    file = open(os.path.join(dirpath, "wnd.wnd"), "w+")
    file.write("Input File wnd.wnd          3/2/2018 ArcSWAT 2012.10_4.19\n")
    return os.path.join(dirpath, "wnd.wnd")


if __name__ == '__main__':
    write_swat_from_db(dirpath)
