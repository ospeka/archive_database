# get swat files and append new data to its end from chosen year
# data chosen from this year(in variable  year_to_append)
# things you should do before using this file:
# 1. update db from pogodaclimate or etc. fill_db_gaps_from_pogodaclimate.py
# 2. write new swat files. use appending_swat_files.py .
# as a source of swat files it takes swat files from write_up_swat_files directory
# 3. use this script to have new swat files. dont forget to update value curr_year.
# as a source of swat files this script takes swat files from swat_files_dir variable(test_write_up dir)
from pprint import pprint
import from_past_year
import datetime
import dateutil
import shutil

res_dir = './from_swat_past_year_test'
swat_files_dir = '../test_write_up'
year_to_append = 2019
curr_year = 2020


def main():
    files = from_past_year.get_files(swat_files_dir)
    pprint(files)
    end_date = datetime.date(year=2020, month=12, day=31)
    today = datetime.date.today()
    days_to_copy = (end_date - today).days
    print(days_to_copy)
    date_to_find = datetime.date(year=year_to_append, month=today.month, day=today.day)
    jan_first = datetime.date(year=date_to_find.year, month=1, day=1)
    day_number = (date_to_find - jan_first).days + 1
    date_to_find_str = str(date_to_find.year) + str(day_number)
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
    to_write_lines = in_file_lines[ind: ind + days_to_copy]
    for to_write in to_write_lines:
        replaced_year = to_write.replace(str(year_to_append), str(curr_year))
        out_file.write(replaced_year)
        # break



if __name__ == '__main__':
    main()
