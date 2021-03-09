import sqlite3
import csv
from pprint import pprint
import pandas as pd

db_path = '../db2.sqlite'

# кинь мені .csv файл з 1 січня 2020 до 4 березня 2021.
def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    res = cursor.execute("""
                    SELECT name
                    FROM sqlite_master
                    WHERE type='table';
                    """).fetchall()
    table_names = [el[0] for el in res]
    # pcps_by_station = []
    dt_index = pd.date_range(start="2020-01-01", end="2021-03-03")
    # pprint(dt_index)
    df = pd.DataFrame(index=dt_index)
    for t_name in table_names:
        print(t_name)
        res = conn.execute(f"""
            SELECT  pcp
            FROM {t_name}
            WHERE dt BETWEEN "2020-01-01" AND "2021-03-04"
        """).fetchall()
        # pprint(res)
        pcps = [el[0] for el in res]
        df[t_name] = pcps
        # break
    print(df)
    df.to_csv('./2020_2021_report.csv')


if __name__ == '__main__':
    main()