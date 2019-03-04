# Here will be functions that append data to
# already created swat files
# 1) append from db from last date till today(or last record in db)
# 2) append data from forecast
# 3) append data as forecast from db previous data
import sqlite3
import os
from pprint import pprint
from datetime import datetime, timedelta
import dateutil.parser as dt_parser

db_path = "./db.sqlite"
write_up_dir = "./test_write_up"


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
    write_up_data(data_to_append, files, write_up_dir)


def write_up_data(data_to_append, files, write_up_dir):
    # add write_up_dir
    pcp_data = []
    test_st = data_to_append[0]
    for record in test_st['data']:
        # add date and pcp in pcp data list
        pcp_data.append([record[0], record[-1]])
    for st in data_to_append[1:]:
        for record, pcp in zip(st['data'], pcp_data):
            pcp.append(record[-1])
    print(files)
    write_up_pcp(pcp_data, files['pcp_file'], write_up_dir)



def write_up_pcp(pcp_data, pcp_file, write_up_dir):
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
            SELECT dt, wind, cloud, tmin, tmax, pcp FROM {}
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
