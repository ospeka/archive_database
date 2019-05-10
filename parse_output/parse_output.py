from pprint import pprint
from collections import OrderedDict
# path to output file
p = "./output.sub"

num_of_subbasins = 116

def parse_output(path):
    file = open(path, mode='r')
    lines = file.readlines()
    data_lines = lines[9:]
    col_names = lines[8].split()

    subbasins = [set_up_dict(col_names) for _ in range(num_of_subbasins)]
    first_line = data_lines[0].split()[1:]
    it = iter(subbasins[0].keys())
    i = 0
    for line in data_lines:
        it = iter(subbasins[i].keys())
        for key, val in zip(it, line.split()[1:]):
            if key == 'MON':
                splited = val.split('.')
                area = float('0.' + splited[1])
                subbasins[i]['MON'].append(int(splited[0]))
                subbasins[i]['AREAkm2'].append(area)
                next(it)
                continue
            subbasins[i][key].append(float(val))
        i += 1
        if i == 116:
            i = 0
    # pprint(subbasins[0])
    return subbasins


def set_up_dict(col_names):
    subbasin = OrderedDict()
    for col_name in col_names:
        if col_name == 'mg/L':
            continue
        if col_name == 'ORGPkg/haNSURQkg/ha':
            subbasin['ORGPkg/ha'] = []
            subbasin['NSURQkg/ha'] = []
            continue
        if col_name == 'LAT':
            subbasin['LAT Q(mm)'] = []
            continue
        if col_name == 'Q(mm)LATNO3kg/hGWNO3kg/haCHOLAmic/LCBODU':
            subbasin['LATNO3kg/h'] = []
            subbasin['GWNO3kg/ha'] = []
            subbasin['CHOLAmic/L'] = []
            subbasin['CBODU mg/L'] = []
            continue
        if col_name == 'DOXQ':
            subbasin['DOXQ mg/L'] = []
            continue
        subbasin[col_name] = []
    
    return subbasin


def get_vals(col_name, subbasins, start_date=False, end_date=False, day=1):
    if not start_date and not end_date:
        vals = []
        for subbasin in subbasins:
            vals.append(subbasin[col_name][day - 1])
        return vals
    if start_date and end_date:
        pass

def get_vals_for_hidrograph(subbasins, start_date=False, end_date=False, day=1):
    if not start_date and not end_date:
        pass


if __name__ == '__main__':
    parse_output(p)
