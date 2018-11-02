import re


def count_avg(recs):
    return sum([float(rec) for rec in recs]) / len(recs)


def count_sum(recs):
    return sum([float(rec) for rec in recs])


def isfloat(s):
    try:
        float(s)
    except ValueError:
        return False
    return True

class DayRecord:
    # re patterns here
    cloud_patt = re.compile(r'\d{1,2}/')
    wind_patt1 = re.compile(r'\d{1,3}\{\d{1,5}\}')
    wind_patt2 = re.compile(r'5-11{13}')

    def __init__(self, start=0, end=0, month_data=[], date=None):
        self.date = date
        self.wind = month_data['wind'][start:end]
        self.recount_wind()
        self.cloud = month_data['cloud'][start:end]
        self.recount_cloud()
        self.t = month_data['T'][start:end]
        self.recount_t()
        self.tmin = month_data['Tmin'][start:end]
        self.recount_tmin()
        self.tmax = month_data['Tmax'][start:end]
        self.recount_tmax()
        #pcp == R  == опади
        self.pcp = month_data['R'][start:end]
        self.recount_pcp()
        #s - snow height
        self.s = month_data['S'][start:end]
        self.recount_s()
        #hum == humidity == f
        self.hum = month_data['f'][start:end]
        self.recount_hum()
        self.td = month_data['Td'][start:end]

    def recount_hum(self):
        hum_recs = []
        for rec in self.hum:
            if isfloat(rec):
                hum_recs.append(rec)
        if hum_recs:
            self.hum = round(count_avg(hum_recs) / 100, 2)
        else:
            self.hum = None

    def recount_s(self):
        s_recs = []
        for rec in self.s:
            if isfloat(rec):
                s_recs.append(rec)
        if s_recs:
            self.s = round(count_avg(s_recs), 2)
        else:
            self.s = None

    def recount_pcp(self):
        pcp_nums = []
        for rec in self.pcp:
            if isfloat(rec):
                pcp_nums.append(float(rec))
        if pcp_nums:
            self.pcp = round(sum(pcp_nums), 2)
        else:
            self.pcp = None

    def recount_tmax(self):
        t_max_nums = []
        for rec in self.tmax:
            if isfloat(rec):
                t_max_nums.append(float(rec))
        if t_max_nums:
            self.tmax = min(t_max_nums)
        else:
            self.tmax = None

    def recount_tmin(self):
        t_min_nums = []
        for rec in self.tmin:
            if isfloat(rec):
                t_min_nums.append(float(rec))
        if t_min_nums:
            self.tmin = min(t_min_nums)
        else:
            self.tmin = None

    def recount_t(self):
        t_recs = []
        for rec in self.t:
            if isfloat(rec):
                t_recs.append(rec)
        if t_recs:
            self.t = round(count_avg(t_recs), 2)
        else:
            self.t = None

    def recount_wind(self):
        wind_recs = []
        for rec in self.wind:
            if isfloat(rec):
                wind_recs.append(float(rec))
                continue
            elif DayRecord.wind_patt1.match(rec):
                bracket_ind = rec.index('{')
                wind_recs.append(float(rec[:bracket_ind]))
                continue
            elif DayRecord.wind_patt2.match(rec):
                minus_ind = rec.index('-')
                bracket_ind = rec.index('{')
                first = float(rec[:minus_ind])
                second = float(rec[minus_ind + 1:bracket_ind])
                wind_recs.append((first + second) / 2)
                continue
        if wind_recs:
            self.wind = round(count_avg(wind_recs), 2)
        else:
            self.wind = None



    def recount_cloud(self: list):
        cloud_recs = []
        for rec in self.cloud:
            if rec == 'ясно':
                cloud_recs.append(0)
                continue
            if DayRecord.cloud_patt.match(rec):
                slash_index = rec.index('/')
                cloud_recs.append(rec[:slash_index])
        if len(cloud_recs) == 0:
            self.cloud = None
            return
        self.cloud = round(count_avg(cloud_recs), 2)






