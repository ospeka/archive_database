#   + наблюдения из прошлого за какой-то год
import os
from pprint import pprint
import sqlite3
import json
from collections import OrderedDict
from datetime import datetime as dt
from datetime import timedelta
import csv

directory = "../SWAT_united_test"
year = 2018
days = 60
db_path = "../db.sqlite"
city_translit_path = "../city_translit.json"
irrad_file = "../forecast/Солнечная_радиация_станд_значения.csv"
a = 0.4
b = 0.38
Cor_factor = 0.4

def from_past_year(directory):
    files = get_files(directory)
    pprint(files)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    translit = json.loads(open(city_translit_path, mode='r').read(), object_pairs_hook=OrderedDict)
    stations = translit.values()
    translit = {val: key for key, val in translit.items()}
    pprint(stations)
    today = dt.today().date()
    start_date = dt(year=year, month=today.month, day=today.day)
    pprint(start_date)
    end_date = start_date + timedelta(days=days)
    pprint(end_date)
    write_pcp_data(cursor, stations, start_date, end_date, files['pcp_file'])
    write_temp_data(cursor, stations, start_date, end_date, files['temp_file'])
    write_wind_data(cursor, stations, start_date, end_date, files['wind_file'])
    write_hum_data(cursor, stations, start_date, end_date, files['hum_file'])
    write_slr_data(cursor, stations, start_date, end_date, files['slr_file'], translit)
    conn.close()


def write_slr_data(cursor, stations, start_date, end_date, slr_file, translit):
    clouds_data = get_clouds_data_from_db(cursor, stations, start_date, end_date)
    file = open(slr_file, mode='a')
    with open(irrad_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        irr_data = [line for line in reader]
    days_count = days
    curr_date = dt.today().date()
    i = 0
    one_day = timedelta(days=1)
    while i < days_count:
        first_jan = dt(int(curr_date.year), 1, 1).date()
        delta = curr_date - first_jan
        curr_year = curr_date.year
        file.write("{}{:03}".format(curr_year, delta.days + 1))
        for st in clouds_data:
            try:
                clouds = st['data'][i][1]
                # recount to solar radiation here
                slr = use_formula(clouds, irr_data, curr_date, st['name'], translit)
            except IndexError:
                print(st['name'])
                print(i)
            try:
                file.write("{:08.3f}".format(slr))
            except TypeError:
                print(st['name'], date, clouds, slr)
        curr_date += one_day
        file.write("\n")
        i += 1

def use_formula(clouds, irr_data, date, st_name, translit):
    st_translit = translit[st_name]
    st_index = irr_data[0].index(st_translit)
    month_index = date.month
    q_zero = float(irr_data[month_index][st_index])
    n = clouds / 10
    slr = q_zero * (1 - (a + b * n) * n)
    slr *= (1 + Cor_factor)
    return round(slr, 3)

def get_clouds_data_from_db(cursor, stations, start_date, end_date):
    data = []
    for st_name in stations:
        st_data = {}
        st_data['name'] = st_name
        st_records = cursor.execute("""
            SELECT dt, cloud from {}
            WHERE dt >= (?) and dt < (?)
            ORDER BY dt
            """.format(st_name), (str(start_date), str(end_date))).fetchall()
        st_data['data'] = st_records
        data.append(st_data)
    return data


def write_hum_data(cursor, stations, start_date, end_date, hum_file):
    hum_data = get_hum_data_from_db(cursor, stations, start_date, end_date)
    file = open(hum_file, mode='a')
    days_count = days
    curr_date = dt.today().date()
    i = 0
    one_day = timedelta(days=1)
    while i < days_count:
        first_jan = dt(int(curr_date.year), 1, 1).date()
        delta = curr_date - first_jan
        curr_year = curr_date.year
        file.write("{}{:03}".format(curr_year, delta.days + 1))
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
        curr_date += one_day
        file.write("\n")
        i += 1


def get_hum_data_from_db(cursor, stations, start_date, end_date):
    data = []
    for st_name in stations:
        st_data = {}
        st_data['name'] = st_name
        st_records = cursor.execute("""
            SELECT dt, hum from {}
            WHERE dt >= (?) and dt < (?)
            ORDER BY dt
            """.format(st_name), (str(start_date), str(end_date))).fetchall()
        st_data['data'] = st_records
        data.append(st_data)
    return data


def write_wind_data(cursor, stations, start_date, end_date, wind_file):
    wind_data = get_wind_data_from_db(cursor, stations, start_date, end_date)
    file = open(wind_file, mode='a')
    days_count = days
    curr_date = dt.today().date()
    i = 0
    one_day = timedelta(days=1)
    while i < days_count:
        first_jan = dt(int(curr_date.year), 1, 1).date()
        delta = curr_date - first_jan
        curr_year = curr_date.year
        file.write("{}{:03}".format(curr_year, delta.days + 1))
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
        curr_date += one_day
        file.write("\n")
        i += 1


def get_wind_data_from_db(cursor, stations, start_date, end_date):
    data = []
    for st_name in stations:
        st_data = {}
        st_data['name'] = st_name
        st_records = cursor.execute("""
            SELECT dt, wind from {}
            WHERE dt >= (?) and dt < (?)
            ORDER BY dt
            """.format(st_name), (str(start_date), str(end_date))).fetchall()
        st_data['data'] = st_records
        data.append(st_data)
    return data


def write_temp_data(cursor, stations, start_date, end_date, temp_file):
    temp_data = get_temp_data_from_db(cursor, stations, start_date, end_date)
    file = open(temp_file, mode='a')
    days_count = days
    curr_date = dt.today().date()
    i = 0
    one_day = timedelta(days=1)
    while i < days_count:
        first_jan = dt(int(curr_date.year), 1, 1).date()
        delta = curr_date - first_jan
        curr_year = curr_date.year
        file.write("{}{:03}".format(curr_year, delta.days + 1))
        for st in temp_data:
            try:
                max_temp = st['data'][i][1]
                min_temp = st['data'][i][2]
            except IndexError:
                print(st['name'])
                print(i)
            file.write("{:-05.1f}".format(float(max_temp)))
            file.write("{:-05.1f}".format(float(min_temp)))
        curr_date += one_day
        file.write("\n")
        i += 1

def get_temp_data_from_db(cursor, stations, start_date, end_date):
    data = []
    for st_name in stations:
        st_data = {}
        st_data['name'] = st_name
        st_records = cursor.execute("""
            SELECT dt, tmax, tmin from {}
            WHERE dt >= (?) and dt < (?)
            ORDER BY dt
            """.format(st_name), (str(start_date), str(end_date))).fetchall()
        st_data['data'] = st_records
        data.append(st_data)
    return data


def write_pcp_data(cursor, stations, start_date, end_date, pcp_file):
    pcp_data = get_pcp_data_from_db(cursor, stations, start_date, end_date)
    file = open(pcp_file, mode='a')
    days_count = days
    curr_date = dt.today().date()
    i = 0
    one_day = timedelta(days=1)
    while i < days_count:
        first_jan = dt(int(curr_date.year), 1, 1).date()
        delta = curr_date - first_jan
        curr_year = curr_date.year
        file.write("{}{:03}".format(curr_year, delta.days + 1))
        for st in pcp_data:
            try:
                day_pcp = st['data'][i][1]
            except IndexError:
                print(st['name'])
                print(i)
            if day_pcp is None or not day_pcp:
                day_pcp = 0.0
            file.write("{:05.1f}".format(float(day_pcp)))
        curr_date += one_day
        file.write("\n")
        i += 1


def get_pcp_data_from_db(cursor, stations, start_date, end_date):
    data = []
    for st_name in stations:
        st_data = {}
        st_data['name'] = st_name
        st_records = cursor.execute("""
            SELECT dt, pcp from {}
            WHERE dt >= (?) and dt < (?)
            ORDER BY dt
            """.format(st_name), (str(start_date), str(end_date))).fetchall()
        st_data['data'] = st_records
        data.append(st_data)
    return data


def get_files(directory):
    dir_content = os.listdir(directory)
    files = {}
    for file_name in dir_content:
        if ".hmd" in file_name:
            files['hum_file'] = os.path.join(directory, file_name)
            continue
        if ".pcp" in file_name:
            files['pcp_file'] = os.path.join(directory, file_name)
            continue
        if ".slr" in file_name:
            files['slr_file'] = os.path.join(directory, file_name)
            continue
        if ".tmp" in file_name:
            files['temp_file'] = os.path.join(directory, file_name)
            continue
        if ".wnd" in file_name:
            files['wind_file'] = os.path.join(directory, file_name)
    return files


if __name__ == '__main__':
    from_past_year(directory)
