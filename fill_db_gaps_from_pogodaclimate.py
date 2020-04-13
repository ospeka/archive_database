from datetime import datetime
import sqlite3
from dateutil.relativedelta import relativedelta
import json
import os
from pprint import pprint

import json_downloader
import json_parser
import update_db

get_params = {
    "id": "26898",
    "bday": "1",
    "fday": "10",
    "amonth": "10",
    "ayear": "2018",
    "bot": "2"
}

db_path = './db2020.sqlite'
start_date = datetime(year=2011, month=1, day=1)
end_date = datetime.now()
end_date = datetime(year=end_date.year, month=end_date.month, day=end_date.day)
city_ids_path = "./city_ids.json"
update_data_dir = "./update_data/"

def main():
    con = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = con.cursor()
    days_num = (end_date - start_date).days
    print(days_num)
    res = cursor.execute("""
           SELECT name
           FROM sqlite_master
           WHERE type='table';
           """).fetchall()
    table_names = [el[0] for el in res]
    st_to_upd = select_st_to_upd(cursor, days_num, table_names)
    pprint(st_to_upd)
    print(len(st_to_upd))
    # fill_gaps(cursor, st_to_upd[0])
    for st_name in st_to_upd:
        fill_gaps(cursor, st_name)
    con.commit()
    con.close()


def fill_gaps(cursor, st):
    one_day = relativedelta(days=1)
    gap_days = []
    curr_date = start_date
    while curr_date != end_date:
        res = cursor.execute(f"""
            SELECT * FROM {st}
            WHERE dt=(?)
        """, (str(curr_date),)).fetchall()
        if not res:
            gap_days.append(curr_date)
        curr_date += one_day
    print(st, gap_days)
    # st_data, upd_file_path = get_data_to_fill(gap_days[0], st)
    for gap_day in gap_days:
        st_data, upd_file_path = get_data_to_fill(gap_day, st)
        if os.path.isfile(upd_file_path):
            os.remove(upd_file_path)
        else:
            print(f"Error: {upd_file_path} file not found")
        update_db.insert_update(st_data, st, cursor)



def get_data_to_fill(gap_day, st_name):
    city_ids = json.load(open(city_ids_path, "r"))
    data_list = [{'city': st_name, 'city_id': city_ids[st_name]}]
    get_params['bday'] = gap_day.day
    get_params['fday'] = gap_day.day
    get_params['amonth'] = gap_day.month
    get_params['ayear'] = gap_day.year
    get_params['id'] = city_ids[st_name]
    dates_table, data_table = json_downloader.get_table(get_params)
    data = json_downloader.parse_table(dates_table, data_table)
    data['date'].append({'year': get_params["ayear"]})
    data['year'] = str(gap_day.year)
    data_list.append(data)
    path = update_data_dir + st_name + "_upd_data.json"
    with open(path, 'w+') as fout:
        json.dump(data_list, fout)
    st_data, st_name_from_json = json_parser.get_city_data(path=path)
    return st_data, path



def select_st_to_upd(cursor, days_num, table_names):
    """
    :param cursor: db cursor for executing requests
    :param days_num: num of days from starts of recording
    :param table_names: list of table names
    :return: list of table names which need to be updated
    """
    to_upd = []
    for name in table_names:
        res = cursor.execute("""
            SELECT count(*) FROM {};
        """.format(name)).fetchall()
        if res[0][0] != days_num:
            to_upd.append(name)
    return to_upd


if __name__ == '__main__':
    main()