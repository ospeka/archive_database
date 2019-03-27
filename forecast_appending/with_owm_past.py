# прогноз на 4 дня (openweathermap)+ наблюдения из прошлого
# дані за сьогодійшній день це середнє між прогнозом 
# на завтра і спостереженнями за вчора
import sys
sys.path.append('../')
import forecast.forecast as fc
from from_past_year import get_files
from pprint import pprint
from datetime import datetime, timedelta
import sqlite3
import json

directory = "../SWAT_united_test"
db_path = "../db.sqlite"
translit_path = "../city_translit.json"

def main():
    stations = fc.create_stations()
    stations = fc.perform_calcs(stations)
    files = get_files(directory)
    for st in stations:
        print(st)
    write_today(stations)

    # write_clouds(stations, files['slr_file'])
    # write_hum(stations, files['hum_file'])
    # write_pcp(stations, files['pcp_file'])
    # write_temp(stations, files['temp_file'])
    # write_wind(stations, files['wind_file'])

def write_today(stations):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    translit = json.load(open(translit_path))
    tables = cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table';
    """).fetchall()
    tables = [el[0] for el in tables]
    pcp_list = []
    for st in stations:
        pcp = count_avg_pcp(cursor, st, translit)
        pcp_list.append(pcp)

    print(pcp_list)


def count_avg_pcp(cursor, st, translit):
    tommorow = min(st.pcp.keys())
    tommorow_pcp = st.pcp[tommorow]
    translited = translit[st.name]
    two_days = timedelta(days=2)
    yesterday = tommorow - two_days
    print(yesterday)
    print(type(yesterday))
    print(translited)
    yesterday_pcp = cursor.execute("""
        SELECT pcp FROM {}
        WHERE dt=(?)
        """.format(translited), yesterday).fetchall()
    return (yesterday_pcp + tommorow_pcp) / 2


def write_wind(stations, wind_file):
    file = open(wind_file, mode='a')
    days = stations[0].pcp.keys()
    for day in days:
        file.write(str(day.year))
        first_jan = datetime(int(day.year), 1, 1)
        delta = day - first_jan
        file.write("{:03}".format(delta.days + 1))
        for st in stations:
            file.write("{:08.3f}".format(st.wind[day]))
        file.write('\n')


def write_temp(stations, temp_file):
    file = open(temp_file, mode='a')
    days = stations[0].pcp.keys()
    for day in days:
        file.write(str(day.year))
        first_jan = datetime(int(day.year), 1, 1)
        delta = day - first_jan
        file.write("{:03}".format(delta.days + 1))
        for st in stations:
            file.write("{:-05.1f}".format(st.temp[day]["max_temp"]))
            file.write("{:-05.1f}".format(st.temp[day]["min_temp"]))
        file.write('\n')


def write_pcp(stations, pcp_file):
    file = open(pcp_file, mode='a')
    days = stations[0].pcp.keys()
    for day in days:
        file.write(str(day.year))
        first_jan = datetime(int(day.year), 1, 1)
        delta = day - first_jan
        file.write("{:03}".format(delta.days + 1))
        for st in stations:
            file.write("{:05.1f}".format(st.pcp[day]))
        file.write('\n')


def write_hum(stations, hum_file):
    file = open(hum_file, mode='a')
    days = stations[0].pcp.keys()
    for day in days:
        file.write(str(day.year))
        first_jan = datetime(int(day.year), 1, 1)
        delta = day - first_jan
        file.write("{:03}".format(delta.days + 1))
        for st in stations:
            file.write("{:08.3f}".format(st.hmd[day]))
        file.write('\n')


def write_clouds(stations, slr_file):
    file = open(slr_file, mode='a')
    days = stations[0].pcp.keys()
    for day in days:
        file.write(str(day.year))
        first_jan = datetime(int(day.year), 1, 1)
        delta = day - first_jan
        file.write("{:03}".format(delta.days + 1))
        for st in stations:
            file.write("{:08.3f}".format(st.clouds[day]))
        file.write('\n')


if __name__ == '__main__':
    main()
