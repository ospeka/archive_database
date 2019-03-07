from datetime import datetime as dt

s = "01.01.2018"

dt_obj = dt.strptime(s, "%d.%m.%Y")

print(dt_obj)
