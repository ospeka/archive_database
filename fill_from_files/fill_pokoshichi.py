import csv
from pprint import pprint
import datetime as dt
import sqlite3

# Покошичі 2015-2017 з цлього файлу

p = './Pokoshichi_2015_2017.txt'
start_date = dt.date(year=2015, month=1, day=1)
end_date = dt.date(year=2018, month=1, day=1)
one_day = dt.timedelta(days=1)
db_path = '../db2.sqlite'

def main():
    reader = csv.reader(open(p), delimiter='\t')
    lines = [line for line in reader]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    curr_date = start_date
    for line in lines:
        if curr_date == end_date:
            break
        date_from_csv = dt.datetime.strptime(line[0], '%m/%d/%Y')
        # print(date_from_csv)
        if curr_date != date_from_csv.date():
            print(curr_date)
            print(date_from_csv)
            raise Exception("its bad")
        pcp = float(line[1])
        curr_dt = dt.datetime(year=curr_date.year, month=curr_date.month, day=curr_date.day)
        res = cursor.execute("""
                    UPDATE Pokoshichi
                    SET pcp = ?
                    WHERE dt = ?
                """, (pcp, curr_dt)).fetchall()
        print(res)
        curr_date += one_day
        # break
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
