# updating from pogodaklimat site
import sqlite3
import datetime as dt
import dateutil.parser as dp
from dateutil.relativedelta import relativedelta
from json_downloader import get_table, parse_table
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

cities = [
    "Bryansk",
    "Dmitrovsk",
    "Elnya",
    "Fatezh",
    "Karachaev",
    "Kurchatov",
    "Kursk",
    "Navlya",
    "Oboyan",
    "Poniri",
    "Rilsk",
    "SpasDemensk",
    "Tim",
    "Trubchevsk",
    "Unecha",
    "Zhizdra",
    "Zhukovka",
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
db_path = "./db.sqlite"
city_ids_path = "./city_ids.json"
update_data_dir = "./update_data/"

def main():
    update_db(db_path, city_ids_path, update_data_dir)


def update_db(db_path, city_ids_path, update_data_dir):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    at_least_one_uppdate_done = False
    for city in cities:
        path = download_data(city, cursor, city_ids_path, update_data_dir)
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
        at_least_one_uppdate_done = True
    con.commit()
    con.close()
    return at_least_one_uppdate_done


def insert_update(data, city_name, cursor):
    for rec in data:
        cursor.execute("""
            INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?)
            """.format(city_name),(None, rec.date, rec.wind, rec.cloud, rec.t, rec.tmin, rec.tmax, rec.pcp, rec.s, rec.hum))
    print("Update done.")


def download_data(city, cursor, city_ids_path, update_data_dir):
    """
    download data and save it in json file
    with path = "./update_data./upd_data.json"
    :param city:name of city to download data
    :param cursor cursor to sqlite db
    :return: path to downloaded data or None when update doesnt needed
    """
    max_date = cursor.execute("""
        SELECT MAX(dt) FROM {}
        """.format(city)).fetchall()[0][0]
    start_date = dp.parse(max_date)
    one_day = relativedelta(days=1)
    end_date = dt.date.today() - one_day
    curr_date = start_date
    data_list = []
    city_ids = json.load(open(city_ids_path, "r"))
    data_list.append({'city': city, 'city_id': city_ids[city]})
    if compare_date(curr_date, end_date):
        return None
    while compare_date(curr_date, end_date) is False:
        curr_date += one_day
        get_params['bday'] = curr_date.day
        get_params['fday'] = curr_date.day
        get_params['amonth'] = curr_date.month
        get_params['ayear'] = curr_date.year
        get_params['id'] = city_ids[city]
        table = get_table(get_params)
        data = parse_table(table)
        data['date'].append({'year': get_params["ayear"]})
        data['year'] = str(curr_date.year)
        data_list.append(data)
    path = update_data_dir + city + "_upd_data.json"
    with open(path, 'w+') as fout:
        json.dump(data_list, fout)
    return path


def compare_date(date1, date2):
    if date1.year != date2.year:
        return False
    if date1.month != date2.month:
        return False
    if date1.day != date2.day:
        return False
    return True


if __name__ == '__main__':
    main()
