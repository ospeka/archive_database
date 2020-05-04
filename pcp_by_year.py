import sqlite3
from pprint import pprint

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
    for name in table_names:
        res = cursor.execute(f"""
            SELECT SUM(pcp)            AS total_amount, 
            Strftime("%Y", `dt`) AS 'month' 
            FROM   {name}
            GROUP  BY Strftime("%Y", `dt`); 
        """).fetchall()
        print(name)
        for el in res:
            print(el[1], ' - ', round(el[0], 3))

if __name__ == '__main__':
    main()