import pandas as pd
import sqlite3

db_path = '../db2.sqlite'
table_path = './manual.csv'


def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    df = pd.read_csv(table_path, index_col=0, parse_dates=True)
    df.fillna(value=0, axis='columns', inplace=True)
    print(df)
    print(type(df.index))
    for column in df.columns:
        print(column)
        # print(type(column))
        col_series = df[column]
        print(col_series)
        for index, pcp in col_series.iteritems():
            # print(index, pcp)
            dt = index.strftime('%Y-%m-%d') + " 00:00:00"
            res = cursor.execute(f"""
                UPDATE {column}
                SET pcp = {pcp}
                WHERE dt = "{dt}"
            """)
            # print(res)
            # print(type(index))
            # print(type(pcp))
            # break
        # break
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
