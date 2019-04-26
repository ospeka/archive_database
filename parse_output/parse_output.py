# path to output file
p = "./output.sub"


def parse_output(path):
    file = open(path, mode='r')
    lines = file.readlines()
    data_lines = lines[9:]
    col_names = lines[8].split()

    subbasins = [set_up_dict(col_names) for _ in range(116)]
    i = 0
    flag = 0
    for line in data_lines:
        for col_name, meas in zip(col_names, line.split()):
            try:
                if flag == 1 and col_name == 'mg/L':
                    subbasins[i]['mg/L 2'].append(float(meas))
                    flag = 0
                    continue
                if col_name == 'mg/L':
                    flag = 1
                subbasins[i][col_name].append(float(meas))
            except ValueError:
                subbasins[i][col_name].append(meas)
        i += 1
        if i == 116:
            i = 0
    return subbasins


def set_up_dict(col_names):
    subbasin = {}
    for col_name in col_names:
        subbasin[col_name] = []
    subbasin['mg/L 2'] = []
    return subbasin


def get_vals(col_name, subbasins, start_date=False, end_date=False, day=1):
    if not start_date and not end_date:
        vals = []
        for subbasin in subbasins:
            vals.append(subbasin[col_name][day - 1])
        return vals
    if start_date and end_date:
        pass


if __name__ == '__main__':
    parse_output(p)
