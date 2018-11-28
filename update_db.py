import sqlite3
from pprint import pprint
import datetime as dt
import dateutil.parser as dp
from dateutil.relativedelta import relativedelta
from csv_downloader import get_table, parse_table
import json
from json_parser import get_city_data
import os

get_params = {
    "id": "26898",
    "bday": "1",
    "fday": "10",
    "amonth": "10",
    "ayear": "2018",
    "bot": "2"
}


def main():
    update_db()


def update_db():
    con = sqlite3.connect('./db.sqlite')
    cursor = con.cursor()
    cursor.execute("""
        		SELECT name FROM sqlite_master WHERE type='table';
        	""")
    tables = cursor.fetchall()
    cities = [el[0] for el in tables]
    for city in cities:
        path = download_data(city, cursor)
        if path is None:
            print("Update for ", city, " doesnt need.")
            continue
        print(path)
        city_data, city_name = get_city_data(path)
        if os.path.isfile(path):
            os.remove(path)
        else:
            print("Error: %s file not found" % path)
        insert_update(city_data, city_name, cursor)
    con.commit()
    con.close()


def insert_update(data, city_name, cursor):
    for rec in data:
        cursor.execute("INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?)".format(city_name),
                       (None, rec.date, rec.wind, rec.cloud, rec.t, rec.tmin, rec.tmax, rec.pcp, rec.s, rec.hum))
    print("Update done.")


def download_data(city, cursor):
    """
    download data and save it in json file with path = "./update_data./upd_data.json"
    :param city:name of city to download data
    :param cursor cursor to sqlite db
    :return: path to downloaded data or None when update doesnt needed
    """
    max_date = cursor.execute("SELECT MAX(dt) FROM {}".format(city)).fetchall()[0][0]
    start_date = dp.parse(max_date)
    end_date = dt.date.today()
    one_day = relativedelta(days=1)
    curr_date = start_date
    data_list = []
    city_ids = json.load(open("./city_ids.json", "r"))
    data_list.append({'city': city, 'city_id': city_ids[city]})
    if curr_date.day == end_date.day and curr_date.month == end_date.month and curr_date.year == end_date.year:
        return None
    while curr_date.day != end_date.day:
        curr_date += one_day
        get_params['bday'] = curr_date.day
        get_params['fday'] = curr_date.day
        get_params['amonth'] = curr_date.month
        get_params['ayear'] = curr_date.year
        table = get_table(get_params)
        data = parse_table(table)
        data['date'].append({'year': get_params["ayear"]})
        data['year'] = str(curr_date.year)
        data_list.append(data)
    path = "./update_data/" + city + "_upd_data.json"
    with open(path, 'w+') as fout:
        json.dump(data_list, fout)
    return path

if __name__ == '__main__':
    main()
