import sqlite3

conn = sqlite3.connect("./db.sqlite")
cursor = conn.cursor()
tables = cursor.execute("""
    SELECT name FROM sqlite_master WHERE type='table';
    """).fetchall()
tables = [el[0] for el in tables]
for st in tables:
    no_tmp_data = cursor.execute("""
        SELECT dt, tmin, tmax FROM {} WHERE tmin is NULL or tmax is NULL or t is NULL
        ORDER BY dt
        """.format(st)).fetchall()
    print(st)
    if no_tmp_data:
        for el in no_tmp_data:
            print(el)
