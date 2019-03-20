from datetime import datetime
from pprint import pprint

first = datetime(year=2019, day=1, month=1)
second = datetime(year=2019, day=1, month=2)

l = [first, second]

print(max(l))
