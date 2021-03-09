import sqlite3
from pprint import pprint
import csv
import pandas as pd
import pathlib

db_path = './sula_db.sqlite'

def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    res = cursor.execute("""
                    SELECT name
                    FROM sqlite_master
                    WHERE type='table';
                    """).fetchall()
    table_names = [el[0] for el in res]
    # pprint(res)
    for table_name in table_names:
        write_csv(cursor, table_name)
    convert_csv_to_excel()
    conn.commit()
    conn.close()


def convert_csv_to_excel():
    dir_path = pathlib.Path('./csvs')
    writer = pd.ExcelWriter('./sula_data.xlsx', engine='xlsxwriter')
    for filepath in dir_path.iterdir():
        df = pd.read_csv(filepath)
        df['dt'] = pd.to_datetime(df['dt'], format='%Y-%m-%d %H:%M:%S').dt.date
        sheet_name = filepath.stem
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(sheet_name)
        # break
    writer.save()


def write_csv(cursor, table_name):
    res = cursor.execute(f"""
            SELECT dt, t, tmax, tmin, pcp, hum, wind
            FROM {table_name}
            ORDER BY dt ASC 
        """).fetchall()
    out_file = open('csvs/' + table_name + '.csv', mode='w+', newline='')
    writer = csv.writer(out_file)
    writer.writerow(['dt', 't_aver', 't_max', 't_min', 'PCP_cor', 'HMD', 'WND'])
    for el in res:
        writer.writerow(el)

if __name__ == '__main__':
    main()
