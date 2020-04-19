import sqlite3
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib
import datetime as dt
import matplotlib.dates as mdates

stations = 28
db_path = './db2.sqlite'

def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    res = cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table';
            """).fetchall()
    table_names = [el[0] for el in res]
    print(table_names)
    # table_name = table_names[0]
    # fig, axes = plt.subplots(28, 1)
    for i, table_name in enumerate(table_names):
        plt.figure(figsize=(13, 7))
        data = []
        for year in range(2015, 2021):
            res = cursor.execute("""
            SELECT SUM(pcp)            AS total_amount, 
               Strftime("%m", `dt`) AS 'month' 
                FROM   {} 
                WHERE  Strftime("%Y", `dt`) = '{}'
                GROUP  BY Strftime("%m", `dt`); 
            """.format(table_name, str(year))).fetchall()
            # pprint(res)
            for el in res:
                date = dt.date(year=year, month=(int(el[1])), day=1)
                data.append([date, el[0]])
        pprint(data)
        x = [el[0] for el in data]
        y = [el[1] for el in data]
        dates = matplotlib.dates.date2num(x)

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        # axes[i].plot(dates, y)
        # axes[i].grid(color='black')
        plt.plot(dates, y)
        plt.grid(color='black')
        plt.legend([table_name])
        plt.savefig(f'./images/{table_name}')
        # break

    # fig.show()
    plt.show()

if __name__ == '__main__':
    main()