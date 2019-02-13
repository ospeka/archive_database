import forecast.forecast as fc
import sqlite3
from pprint import pprint
import os
import json
import dateutil.parser as dt_parser
from datetime import datetime
import csv

db_path = "./db.sqlite"
dirpath = "./SWAT_united_test"
city_translit = "./city_translit.json"
irrad_file = "./forecast/Солнечная_радиация_станд_значения.csv"
a = 0.4
b = 0.38

def main(stations='all'):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    # # check is directory empty
    stations = fc.create_stations()
    # pass stations here
    stations = fc.perform_calcs(stations)
    files = write_headers(stations, dirpath)
    stations_names = [st.name for st in stations]
    # pprint(stations_names)
    # pprint(files)
    translit = json.load(open(city_translit, mode='r'))
    # write_pcp_from_db(files['pcp_file'], cursor, translit, stations_names)
    # write_temp_from_db(files['temp_file'], cursor, translit, stations_names)
    # write_wind_from_db(files['wind_file'], cursor, translit, stations_names)
    # write_hum_from_db(files['hum_file'], cursor, translit, stations_names)
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
                # recount to sollar radiation here
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
    print(st_index)
    print(month_index)
    q_zero = float(irr_data[month_index][st_index])
    print(q_zero)
    n = clouds / 10
    slr = q_zero * (1 - (a + b * n) * n)
    return round(slr, 3)


def get_clouds_data_from_db(cursor, translit, stations_names):
    data = []
    for st_name in stations_names:
        translited_name = translit[st_name]
        st_data = {}
        st_data['name'] = st_name
        st_data['alter_name'] = translited_name
        st_records = cursor.execute("""
            SELECT dt, cloud from {} ORDER BY dt
            """.format(translited_name)).fetchall()
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
            SELECT dt, hum from {} ORDER BY dt
            """.format(translited_name)).fetchall()
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
            SELECT dt, wind from {} ORDER BY dt
            """.format(translited_name)).fetchall()
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
            SELECT dt, tmax, tmin from {} ORDER BY dt
            """.format(translited_name)).fetchall()
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
            if day_pcp is None:
                day_pcp = 0.0
            file.write("{:05.1f}".format(day_pcp))
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
    return os.path.join(dirpath, "Tmp.tmp")


def write_wind_header(stations, dirpath):
    if (os.sep != '/'):
        dirpath = dirpath.replace('/', os.sep)
    file = open(os.path.join(dirpath, "wnd.wnd"), "w+")
    file.write("Input File wnd.wnd          3/2/2018 ArcSWAT 2012.10_4.19\n")
    return os.path.join(dirpath, "wnd.wnd")


if __name__ == '__main__':
    main()
