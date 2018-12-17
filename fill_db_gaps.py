import sqlite3
from datetime import datetime
from pprint import pprint
from dateutil.relativedelta import relativedelta

db_path = './db.sqlite'
start_date = datetime(year=2011, month=1, day=1)
end_date = datetime.now()
end_date = datetime(year=end_date.year, month=end_date.month, day=end_date.day)

distances = {

}

def main():
    # upd db before filling!!!

    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    days_num = (end_date - start_date).days + 1
    res = cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""").fetchall()
    table_names = [el[0] for el in res]
    pprint(table_names)
    # st_to_upd = select_st_to_upd(cursor, days_num, table_names)

    # for st in st_to_upd:
    # fill_gaps(cursor, st_to_upd[1])

    # print(end_date)
    con.commit()
    con.close()


def fill_gaps(cursor, st):
    print(st)
    one_day = relativedelta(days=1)
    curr_date = start_date
    gap_days = []
    while curr_date != end_date:
        # print(str(curr_date))
        res = cursor.execute("""
            SELECT * FROM {}
            WHERE dt=(?)
        """.format(st), (str(curr_date),)).fetchall()
        if not res:
            gap_days.append(curr_date)
        curr_date += one_day



def select_st_to_upd(cursor, days_num, table_names):
    """
    :param cursor: db cursor for executing requests
    :param days_num: num of days from stasrt of recording
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