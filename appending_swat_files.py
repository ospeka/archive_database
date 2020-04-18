# Here will be functions that append data to
# already created swat files
# 1) append from db from last date till today(or last record in db)
# 2) append data from forecast
# 3) append data as forecast from db previous data
import sqlite3
import os
import csv
from pprint import pprint
from datetime import datetime, timedelta
import dateutil.parser as dt_parser
import write_swat_from_db

db_path = "./db2020.sqlite"
write_up_dir = "./test_write_up"
irrad_file = "./forecast/Солнечная_радиация_станд_значения.csv"

def append_from_db():
    # appends data from db to non till today files
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # write up dir will be dynamic(not global variable)
    files = get_files(write_up_dir)
    # get st names and match it with table names
    tables = cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table';
    """).fetchall()
    tables = [el[0] for el in tables]
    # pprint(tables)
    stations = get_stations(files, tables)
    start_date = get_start_date(files)
    data_to_append = get_data_to_append(start_date, cursor, tables, stations)
    write_up_data(data_to_append, files, stations)


def write_up_data(data_to_append, files, stations):
    # add write_up_dir
    pcp_data = []
    test_st = data_to_append[0]
    for record in test_st['data']:
        # add date and pcp in pcp data list
        pcp_data.append([record[0]])
    for st in data_to_append:
        for record, pcp in zip(st['data'], pcp_data):
            pcp.append(record[-1])

    hmd_data = []
    for record in test_st['data']:
        hmd_data.append([record[0]])
    for st in data_to_append:
        for record, hmd in zip(st['data'], hmd_data):
            hmd.append(record[2])

    cloud_data = []
    for record in test_st['data']:
        cloud_data.append([record[0]])
    for st in data_to_append:
        for record, cloud in zip(st['data'], cloud_data):
            cloud.append(record[-2])

    wnd_data = []
    for record in test_st['data']:
        wnd_data.append([record[0]])
    for st in data_to_append:
        for record, wnd in zip(st['data'], wnd_data):
            wnd.append(record[1])

    tmp_data = []
    for record in test_st['data']:
        tmp_data.append([record[0]])  # t max and tmin
    for st in data_to_append:
        for record, tmp in zip(st['data'], tmp_data):
            tmp.append([record[4], record[3]])  # tmax and tmin
    print()
    # pcp_data, hmd_data, cloud_data, wnd_data, tmp_data

    write_up_pcp(pcp_data, files['pcp_file'])
    write_up_hmd(hmd_data, files['hum_file'])
    write_up_slr(cloud_data, files['slr_file'], stations)
    write_up_wnd(wnd_data, files['wind_file'])
    write_up_tmp(tmp_data, files['temp_file'])

def write_up_tmp(tmp_data, tmp_file):
    file = open(tmp_file, mode='a')
    for day_data in tmp_data:
        date = dt_parser.parse(day_data[0])
        year = date.year
        first_jan = datetime(int(date.year), 1, 1)
        delta = date - first_jan
        file.write("{}{:03}".format(year, delta.days + 1))
        for record in day_data[1:]:
            tmax = record[0] if record[0] else 0.0
            tmin = record[1] if record[1] else 0.0
            file.write("{:-05.1f}".format(float(tmax)))
            file.write("{:-05.1f}".format(float(tmin)))
        file.write('\n')


def write_up_wnd(wnd_data, wnd_file):
    file = open(wnd_file, mode='a')
    for day_data in wnd_data:
        date = dt_parser.parse(day_data[0])
        year = date.year
        first_jan = datetime(int(date.year), 1, 1)
        delta = date - first_jan
        file.write("{}{:03}".format(year, delta.days + 1))
        for record in day_data[1:]:
            wnd = record if record else 0.0
            file.write("{:08.3f}".format(wnd))
        file.write('\n')


def write_up_slr(cloud_data, slr_file, stations):
    file = open(slr_file, mode='a')
    with open(irrad_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        irr_data = [line for line in reader]
    for day_data in cloud_data:
        date = dt_parser.parse(day_data[0])
        year = date.year
        first_jan = datetime(int(date.year), 1, 1)
        delta = date - first_jan
        file.write("{}{:03}".format(year, delta.days + 1))
        for record, st_name in zip(day_data[1:], stations):
            cloud = record if record else 0.0
            slr = write_swat_from_db.use_formula(cloud, irr_data, date, st_name)
            file.write("{:08.3f}".format(slr))
        file.write('\n')

def write_up_hmd(hmd_data, hmd_file):
    file = open(hmd_file, mode='a')
    for day_data in hmd_data:
        date = dt_parser.parse(day_data[0])
        year = date.year
        first_jan = datetime(int(date.year), 1, 1)
        delta = date - first_jan
        file.write("{}{:03}".format(year, delta.days + 1))
        for record in day_data[1:]:
            hmd = record if record else 0.0
            file.write("{:08.3f}".format(hmd))
        file.write('\n')


def write_up_pcp(pcp_data, pcp_file):
    file = open(pcp_file, mode='a')
    for day_data in pcp_data:
        date = dt_parser.parse(day_data[0])
        year = date.year
        first_jan = datetime(int(date.year), 1, 1)
        delta = date - first_jan
        file.write("{}{:03}".format(year, delta.days + 1))
        for record in day_data[1:]:
            pcp = record if record else 0.0
            file.write("{:05.1f}".format(pcp))
        file.write("\n")


def get_data_to_append(start_date, cursor, tables, stations):
    data = []
    for st in stations:
        res = cursor.execute("""
            SELECT dt, wind, hum, tmin, tmax, cloud, pcp FROM {}
            WHERE dt >= (?)
            ORDER BY dt
        """.format(st), (start_date,)).fetchall()
        st_data = {}
        st_data['name'] = st
        st_data['data'] = res
        data.append(st_data)
    return data


def get_start_date(files):
    pcp_file = open(files['pcp_file'], mode='r', encoding='utf-8')
    last_line = pcp_file.readlines()[-1]
    date_str = last_line[:7]
    year = int(date_str[:4])
    days = int(date_str[4:])
    date = datetime(year=year, month=1, day=1)
    delta = timedelta(days=days)
    date += delta
    return date


def get_stations(files, tables):
    pcp_path = files['pcp_file']
    pcp_file = open(pcp_path, mode='r', encoding='utf-8').readlines()
    stations_str = pcp_file[0][9:]
    stations_list = stations_str.split(',')[:-1]
    stations_list = [el.split('_')[0] for el in stations_list]
    if 'Spas-Demensk' in stations_list:
        ind = stations_list.index('Spas-Demensk')
        stations_list[ind] = 'SpasDemensk'
    return stations_list


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
        if ".Tmp" in file_name:
            files['temp_file'] = os.path.join(directory, file_name)
            continue
        if ".wnd" in file_name:
            files['wind_file'] = os.path.join(directory, file_name)
    return files


if __name__ == '__main__':
    append_from_db()
