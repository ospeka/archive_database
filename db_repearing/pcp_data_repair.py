# if no cloud data it will take data from
# nearest station and update it in databease

import sqlite3
from pprint import pprint
import json

st_distances_path = "./station_distances.json"
db_path = "../db2.sqlite"


def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    st_distances = json.load(open(st_distances_path))
    no_cloud_dates = find_no_pcp_dates(cursor)
    pprint(no_cloud_dates)
    for el in no_cloud_dates:
        fill_pcp_gaps(el, st_distances, cursor)
    conn.commit()
    conn.close()


def fill_pcp_gaps(st_data, st_distances, cursor):
    st_name = st_data['station']
    for date in st_data['dates']:
        # print(date)
        data_to_fill = get_data_to_fill(st_name, date, st_distances, cursor)
        if data_to_fill is None:
            continue
        data_to_fill = list(data_to_fill[0])
        data_to_fill.append(date)
        data_to_fill = tuple(data_to_fill)
        cursor.execute("""
            UPDATE {}
            SET pcp = ?
            WHERE dt = ?
        """.format(st_name), data_to_fill)
        pprint(data_to_fill)


def get_data_to_fill(st_name, date, st_distances, cursor):
    i = 0
    print(st_name)
    print(date)
    res = None
    while i < 28:
        print(i)
        try:
            nearest_st = find_nearest_st(st_name, st_distances, i=i)
        except IndexError:
            return None
        print(nearest_st)
        res = cursor.execute("""
            SELECT pcp FROM {}
            WHERE dt=(?)
            """.format(nearest_st), (date,)).fetchall()
        print(res)
        try:
            if all(res[0]) or res[0][0] == 0.0:
                break
            else:
                i += 1
        except IndexError:
            i += 1
            continue
    return res


def find_nearest_st(st, st_distances, i=0):
    needed_st = st_distances[st]
    distances = needed_st.values()
    rev_st_distances = dict([(v, k) for k, v in needed_st.items()])
    dist = sorted(list(distances))[i]
    return rev_st_distances[dist]


def find_no_pcp_dates(cursor):
    tables = cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table';
        """).fetchall()
    tables = [el[0] for el in tables]
    no_tmp_dates = []
    for st in tables:
        no_tmp_data = cursor.execute("""
            SELECT dt, pcp FROM {}
            WHERE pcp is NULL
            ORDER BY dt
            """.format(st)).fetchall()
        if no_tmp_data:
            # print(st)
            records = {}
            records['station'] = st
            records['dates'] = []
            for el in no_tmp_data:
                # print(el)
                records['dates'].append(el[0])
            no_tmp_dates.append(records)
    return no_tmp_dates


if __name__ == "__main__":
    main()
