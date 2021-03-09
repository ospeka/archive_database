import sqlite3
import os

from s_json_parser import get_city_data

db_path = "./sula_db.sqlite"

get_params = {
        "id": "26898",
        "bday": "1",
        "fday": "10",
        "amonth": "10",
        "ayear": "2018",
        "bot": "2"
    }

def main():
    dir_list = os.listdir("./downloaded_data")
    filename, file_extension = os.path.splitext(dir_list[1])
    print(filename, file_extension)
    for file in dir_list:
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".json":
            print("filename - ", filename)
            city_data, city_name = get_city_data(get_params, "./downloaded_data/" + file)
            print(city_name)
            insert_city_data(city_data, city_name)
    # city_data, city_name = get_city_data()
    # insert_city_data(city_data, city_name)


def insert_city_data(city_data, city_name):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table';
    """)
    res = cursor.fetchall()
    for el in res:
        if city_name in el:
            print(city_name, "table exists. Insertions wasn't done")
            return
    cursor.execute("""CREATE TABLE IF NOT EXISTS {} (
    id INTEGER PRIMARY KEY,
    dt datetime,
    wind REAL,
    cloud REAL,
    t REAL,
    tmin REAL,
    tmax REAL,
    pcp REAL,
    s REAL,
    hum REAL
    );""".format(city_name))
    for rec in city_data:
        cursor.execute("INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?)".format(city_name),
                       (None, rec.date, rec.wind, rec.cloud, rec.t, rec.tmin, rec.tmax, rec.pcp, rec.s, rec.hum))
    con.commit()
    print("Insertion done.")
    con.close()


if __name__ == '__main__':
    main()
