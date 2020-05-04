import pandas as pd
import datetime as dt
import csv
import sqlite3
from pprint import pprint
# Август 2016 взять с rp5 для станций рыльск(24), курчатов(23), курск(20), поныри(19), фатеж(16)

p = 'rp5_Desna.xlsx'

# row_2015_start = 7308 2014-12-31
row_2016_08_start = 7886
year_col_num = 2
month_col_num = 3
day_col_num = 4
start_date = dt.date(year=2016, month=8, day=1)
end_date = dt.date(year=2016, month=9, day=1)
one_day = dt.timedelta(days=1)
db_path = '../db2.sqlite'
city_col_num = 16

def main():
    reader = csv.reader(open('./pcp.csv'))
    lines = [line for line in reader]
    # pprint(lines[row_2015_start:])
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    curr_date = start_date
    # print(lines[row_2016_08_start])
    # for i, el in enumerate(lines[2]):
    #     print(i, el)
    for line in lines[row_2016_08_start:]:
        if curr_date == end_date:
            break

        pcp_value = float(line[city_col_num])

        year, month, day = int(line[year_col_num]), int(line[month_col_num]), int(line[day_col_num])
        date_from_csv = dt.date(year=year, month=month, day=day)
        if curr_date != date_from_csv:
            raise Exception("its bad")
        curr_dt = dt.datetime(year=curr_date.year, month=curr_date.month, day=curr_date.day)
        res = cursor.execute("""
            UPDATE Fatezh
            SET pcp = ?
            WHERE dt = ?
        """, (pcp_value, curr_dt)).fetchall()
        # print(res)
        # print(date_from_csv)
        curr_date += one_day
        # break
    conn.commit()
    conn.close()

# .

if __name__ == '__main__':
    main()
