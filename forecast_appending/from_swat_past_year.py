# get swat files and append new data to its end from chosen year
# data chosen from this year(in variable  year_to_append)
# things you should do before using this file:
# 1. update db from pogodaclimate or etc. fill_db_gaps_from_pogodaclimate.py
# 2. write new swat files. use appending_swat_files.py .
# as a source of swat files it takes swat files from write_up_swat_files directory
# 3. use this script to have new swat files. dont forget to update value curr_year.
# as a source of swat files this script takes swat files from swat_files_dir variable(test_write_up dir)
from pprint import pprint
import datetime
import dateutil
import shutil

import from_past_year

year_to_append = 2020
curr_year = 2021
res_dir = f'./scenario_{year_to_append}'
swat_files_dir = '../test_write_up'



def main():
    files = from_past_year.get_files(swat_files_dir)
    pprint(files)
    end_date = datetime.date(year=curr_year + 1, month=1, day=1)
    today = datetime.date.today()
    days_to_copy = (end_date - today).days
    print(days_to_copy)
    date_to_find = datetime.date(year=year_to_append, month=today.month, day=today.day)
    jan_first = datetime.date(year=date_to_find.year, month=1, day=1)
    day_number = (date_to_find - jan_first).days
    date_to_find_str = str(date_to_find.year) + f"{day_number:03}"
    print(date_to_find_str)
    for file in files:
        append_from_swat_file(files[file], date_to_find_str, days_to_copy)
        # break


def append_from_swat_file(swat_file_path, date_to_find_str, days_to_copy):
    print(swat_file_path)
    res_file_path = res_dir + swat_file_path[swat_file_path.find("\\"):]
    print(res_file_path)
    shutil.copyfile(swat_file_path, res_file_path)
    out_file = open(res_file_path, mode='a')
    in_file_lines = open(swat_file_path, mode='r').readlines()
    ind = None
    for line in in_file_lines:
        if line.startswith(date_to_find_str):
            ind = in_file_lines.index(line)
            break

    if year_to_append % 4 != 0:
        # print(in_file_lines[ind + 1])
        to_write_lines = in_file_lines[ind + 1: ind + days_to_copy + 1]
        # print(to_write_lines[-1])
        for to_write in to_write_lines[:-1]:
            replaced_year = to_write.replace(str(year_to_append), str(curr_year))
            out_file.write(replaced_year)
        last_day_line = to_write_lines[-1].replace('001', '366', 1)
        last_day_line = last_day_line.replace(str(year_to_append + 1), str(curr_year))
        out_file.write(last_day_line)
    else:
        to_write_lines = in_file_lines[ind: ind + days_to_copy]
        # print(to_write_lines[0])
        # print(to_write_lines[-1])
        for to_write in to_write_lines:
            replaced_year = to_write.replace(str(year_to_append), str(curr_year))
            out_file.write(replaced_year)



if __name__ == '__main__':
    main()
