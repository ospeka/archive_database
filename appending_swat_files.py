# Here will be functions that append data to
# already created swat files
# 1) append from db from last date till today(or last record in db)
# 2) append data from forecast
import sqlite3
import os
from pprint import pprint
from datetime import datetime, timedelta

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


def get_data_to_append(start_date, cursor, tables, stations):
    # test_st = stations[1]
    # print(test_st)
    # res = cursor.execute("""
    #     SELECT dt, wind, cloud, tmin,tmax, pcp FROM {}
    #     WHERE dt >= (?)
    #     """.format(test_st), (start_date,)).fetchall()
    data = []
    stations[0] = 'SpasDemensk'
    for st in stations:
        res = cursor.execute("""
            SELECT dt, wind, cloud, tmin,tmax, pcp FROM {}
            WHERE dt >= (?)
        """.format(st), (start_date,)).fetchall()
        st_data = {}
        st_data['name'] = st
        st_data['data'] = []
        st_data['data'].append(res)
        data.append(st_data)
    pprint(data)



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
