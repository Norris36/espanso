import datetime

now = datetime.datetime.now()
copenhagen_time = now + datetime.timedelta(hours=7)

print(copenhagen_time.strftime("%H:%M:%S"))
