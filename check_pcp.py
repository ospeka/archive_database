# check pcp difference for stations in give radius
import sqlite3
import json
from pprint import pprint

chosen_distance = 100
year = 2019
# year2 = 2020
st_distances_path = './station_distances.json'
db_path = './db2.sqlite'

def main():
    st_dists = json.load(open(st_distances_path))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for first_st in st_dists:
        res = cursor.execute(f"""
                    SELECT SUM(pcp)
                    FROM {first_st}
                    WHERE strftime("%Y", `dt`) = '{year}' 
                """).fetchall()
        first_st_pcp = res[0][0]
        for second_st in st_dists[first_st]:
            distance = st_dists[first_st][second_st]
            # print(distance)
            if distance >= chosen_distance:
                continue

            res = cursor.execute(f"""
                                SELECT SUM(pcp)
                                FROM {second_st}
                                WHERE strftime("%Y", `dt`) = '{year}' 
                            """).fetchall()
            second_st_pcp = res[0][0]
            difference = abs(first_st_pcp - second_st_pcp)
            if difference >= 100:
                print(first_st, second_st, round(difference, 3))
            # print(difference)
            # break
        # break


if __name__ == '__main__':
    main()
