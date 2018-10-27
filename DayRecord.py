class DayRecord:

    def __init__(self, i, j, month_data=(), date=None):
        self.date = date
        self.wind = round(avg_list(month_data['wind'][i:j]), 2)
        self.cloud = calc_cloud(month_data['cloud'][i:j])
        self.T = round(avg_list(month_data['T'][i:j]), 2)
        # lol
        t_buff = 1000000
        for el in month_data['Tmin'][i:j]:
            if el == "":
                continue
            if float(el) < t_buff:
                t_buff = float(el)
        self.Tmin = t_buff
        t_buff = -273.0
        for el in month_data['Tmax'][i:j]:
            if el == "":
                continue
            if float(el) > t_buff:
                t_buff = float(el)
        self.Tmax = t_buff
        self.R = round(str_list_sum(month_data['R'][i:j]), 2)
        self.S = round(str_list_sum(month_data['S'][i:j]), 2)
        self.f = round(avg_list(month_data['f'][i:j]), 2)
        self.Td = round(avg_list(month_data['Td'][i:j]), 2)

    def __str__(self):
        fields = self.__dict__.keys()
        s = ""
        for field in fields:
            s += str(field) + " "
        s += "\n"
        for field in fields:
            s += str(self.__getattribute__(field)) + " "
        return s


def str_list_sum(lst):
    summary = 0
    for el in lst:
        if el == "":
            continue
        summary += float(el)
    return summary


def avg_list(lst):
    return sum([float(el) for el in lst]) / len(lst)


def calc_cloud(data_slice):
    cloud_nums = []
    for el in data_slice:
        if el == "ясно":
            cloud_nums.append(0)
            continue
        slash_index = el.index('/')
        cloud_nums.append(int(el[:slash_index]))
    return avg_list(cloud_nums)