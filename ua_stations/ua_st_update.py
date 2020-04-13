# File for updating data for ua station.
# Data taken from opened for us ftp server direcory.
# Instead of data for Vyshgorod were taken data for Kyiv.
# means Vishgorod id replaced by Kyiv id!!!

import sqlite3
import json
from pprint import pprint
import dateutil.parser as dt_parser
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt
import datetime
# import ftplib
from math import exp

# f = ftplib.FTP()
# f.connect("uhmi.org.ua", 21)
# f.login("osipov_weather",  "jH9lf26Z")
# f.cwd("osipov_weather")

db_path = "../db2020.sqlite"
ua_ids_path = "./ua_ids.json"

ua_stations = [
    "Chernigiv",
    "Druzhba",
    "Gluchiv",
    "Konotop",
    "Nizhin",
    "Oster",
    "Pokoshichi",
    "Semenivka",
    "Shchors",
    "Sumi",
    "Vishgorod"
]


def ua_st_update(db_path, ua_ids_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    ua_ids = json.load(open(ua_ids_path, mode='r'))
    for st in ua_stations:
        # print(st)
        max_date = get_max_date(st, cursor)
        update_st(max_date, st, cursor, ua_ids)

    conn.commit()
    conn.close()


def get_max_date(st, cursor):
    max_date = cursor.execute("""
        SELECT MAX(dt) FROM {}
        """.format(st)).fetchall()[0][0]
    max_date = dt_parser.parse(max_date)
    return max_date


def update_st(max_date, st, cursor, ua_ids):
    one_day = relativedelta(days=1)
    start_date = max_date + one_day
    # end_date = dt.today()
    # end_date = dt.date(year=2020, month=4, day=7)
    end_date = datetime.datetime(year=2020, month=4, day=7)
    while start_date.date() != end_date.date():
        # print(start_date)
        file_line = get_file_lines(st, start_date, ua_ids)
        if file_line == None:
            start_date += one_day
            continue
        start_date += one_day
        cols = file_line.split(';')
        insert_data(st, cursor, cols)
        # print()

def insert_data(st, cursor, cols):
    dt_obj = dt.strptime(cols[1], "%d.%m.%Y")
    wind = float(cols[2])
    cloud = float(cols[7])
    tmin = float(cols[4])
    tmax = float(cols[5])
    t = (tmin + tmax) / 2
    pcp = float(cols[6])
    s = float(cols[8])
    hum = calc_hum(Td=float(cols[3]), t=t)
    if hum > 1:
        hum = 1
    cursor.execute("""
        INSERT INTO {} 
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """.format(st), (None, dt_obj, wind, cloud, t, tmin, tmax, pcp, s, hum))
    # print(None, dt, wind, cloud, t, tmin, tmax, pcp, s, hum)

def calc_hum(Td=15, t=15):
    rh = (exp((17.625*Td)/(243.04+Td))/exp((17.625*t)/(243.04+t)))
    return round(rh, 3)

def get_file_lines(st, date, ua_ids):
    file_name = compose_file_name(date)
    try:
        file_lines = open(file_name, mode='r').readlines()
    except FileNotFoundError:
        print(file_name)
        return None
    # print(file_name)
    # try:
    #     f.retrlines("RETR ./" + file_name, callback=file_lines.append)
    # except correct exception if file not reachable
    # except:
    #     print(file_name)
    #     print("didnt reach")
    #     return None
    st_id = ua_ids[st]
    for line in file_lines:
        if line.startswith(str(st_id)):
            return line
    return None


def compose_file_name(date):
    file_name = "../osadchii/cgms_"
    if len(str(date.day)) == 1:
        file_name += "0" + str(date.day) + "_"
    else:
        file_name += str(date.day) + "_"
    if len(str(date.month)) == 1:
        file_name += "0" + str(date.month) + "_"
    else:
        file_name += str(date.month) + "_"
    file_name += str(date.year) + ".txt"
    # print(file_name)
    return file_name


if __name__ == '__main__':
    ua_st_update(db_path, ua_ids_path)