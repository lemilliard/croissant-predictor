import datetime

s = "2019-04-01"
d = datetime.datetime.strptime(s, "%Y-%m-%d")
print(d.date())