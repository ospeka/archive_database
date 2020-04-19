import csv
from itertools import zip_longest

rp5_path = './rp5_yearly.csv'
pcp_by_year_path = './pcp_by_year_report.txt'

def main():
    rp5_lines = []
    for line in csv.reader(open(rp5_path)):
        rp5_lines.append(line)

    print(rp5_lines)
    pcp_lines = open(pcp_by_year_path, mode='r').readlines()
    it = grouper(7, pcp_lines)
    for el in it:
        st_name = el[0][:-1]
        pcp1 = el[1].split()[0]
        pcp2 = el[2].split()[0]
        pcp3 = el[3].split()[0]
        print(st_name)

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

if __name__ == '__main__':
    main()