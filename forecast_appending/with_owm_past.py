# прогноз на 4 дня (openweathermap)+ наблюдения из прошлого
# дані за сьогодійшній день це середнє між прогнозом 
# на завтра і спостереженнями за вчора
import sys
sys.path.append('../')
import forecast.forecast as fc
from forecast_appending.from_past_year import get_files
from pprint import pprint
from datetime import datetime, timedelta
import sqlite3
import json

directory = "../SWAT_united_test"
db_path = "../db.sqlite"
translit_path = "../city_translit.json"

def with_owm_past(directory):
    stations = fc.create_stations()
    stations = fc.perform_calcs(stations)
    files = get_files(directory)
    # for st in stations:
        # print(st)
    # writing avg between observation and forecast for today data
    write_today(stations, files)
    # writint forecast data from openweathermap
    write_clouds(stations, files['slr_file'])
    write_hum(stations, files['hum_file'])
    write_pcp(stations, files['pcp_file'])
    write_temp(stations, files['temp_file'])
    write_wind(stations, files['wind_file'])


def write_today(stations, files):
    write_today_pcp(stations, files['pcp_file'])
    write_today_hmd(stations, files['hum_file'])
    write_today_slr(stations, files['slr_file'])
    write_today_tmp(stations, files['temp_file'])
    write_today_wind(stations, files['wind_file'])

def write_today_wind(stations, wind_file):
    file = open(wind_file, mode='r')
    last_line = file.readlines()[-1]
    file.close()
    file = open(wind_file, mode='a')
    write_date(last_line, file)
    start_i = 7
    for st in stations:
        yesterday_wind = float(last_line[start_i:start_i + 8])
        tommorow_date = min(st.wind.keys())
        tommorow_wind = st.wind[tommorow_date]
        avg_wind = (yesterday_wind + tommorow_wind) / 2
        file.write("{:08.3f}".format(avg_wind))
        start_i += 8
    file.write("\n")
    file.close()


def write_today_tmp(stations, temp_file):
    file = open(temp_file, mode='r')
    last_line = file.readlines()[-1]
    file.close()
    file = open(temp_file, mode='a')
    write_date(last_line, file)
    start_i = 7
    for st in stations:
        yesterday_max_temp = float(last_line[start_i: start_i + 5])
        yesterday_min_temp = float(last_line[start_i + 5: start_i + 10])
        tommorow_date = min(st.temp.keys())
        tommorow_max_temp = st.temp[tommorow_date]['max_temp']
        tommorow_min_temp = st.temp[tommorow_date]['min_temp']
        avg_max = (yesterday_max_temp + tommorow_max_temp) / 2
        avg_min = (yesterday_min_temp + tommorow_min_temp) / 2
        file.write("{:-05.1f}".format(avg_max))
        file.write("{:-05.1f}".format(avg_min))
        start_i += 10
    file.write("\n")
    file.close()


def write_today_slr(stations, slr_file):
    file = open(slr_file, mode='r')
    last_line = file.readlines()[-1]
    file.close()
    file = open(slr_file, mode='a')
    write_date(last_line, file)
    start_i = 7
    for st in stations:
        yesterday_slr = float(last_line[start_i:start_i + 8])
        tommorow_date = min(st.clouds.keys())
        tommorow_slr = st.clouds[tommorow_date]
        avg_slr = (yesterday_slr + tommorow_slr) / 2
        file.write("{:08.3f}".format(avg_slr))
        start_i += 8
    file.write("\n")
    file.close()


def write_today_hmd(stations, hum_file):
    file = open(hum_file, mode='r')
    last_line = file.readlines()[-1]
    file.close()
    file = open(hum_file, mode='a')
    write_date(last_line, file)
    start_i = 7
    for st in stations:
        yesterday_hmd = float(last_line[start_i:start_i + 8])
        tommorow_date = min(st.hmd.keys())
        tommorow_hmd = st.hmd[tommorow_date]
        avg_hmd = (yesterday_hmd + tommorow_hmd) / 2
        file.write("{:08.3f}".format(avg_hmd))
        start_i += 8
    file.write("\n")
    file.close()


def write_today_pcp(stations, pcp_file):
    file = open(pcp_file, mode='r')
    last_line = file.readlines()[-1]
    file.close()
    file = open(pcp_file, mode='a')
    write_date(last_line, file)
    start_i = 7
    for st in stations:
        yesterday_pcp = float(last_line[start_i:start_i + 5])
        tommorow_date = min(st.pcp.keys())
        tommorow_pcp = st.pcp[tommorow_date]
        avg_pcp = (yesterday_pcp + tommorow_pcp) / 2
        file.write("{:05.1f}".format(avg_pcp))
        start_i += 5
    file.write("\n")
    file.close()


def write_date(last_line, file):
    year = int(last_line[:4])
    day = int(last_line[4:7])
    date = datetime(year=year, month=1, day=1)
    days = timedelta(days=(day+1))
    date += days
    file.write(str(date.year))
    first_jan = datetime(year=year, month=1, day=1)
    delta = date - first_jan
    file.write("{:03}".format(delta.days))


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
    with_owm_past(directory)
