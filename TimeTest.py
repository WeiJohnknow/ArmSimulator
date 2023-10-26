import datetime

current_datetime = datetime.datetime.now()
current_time_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
print("Current Date and Time:", current_datetime)
current_time = current_datetime.time()
print("Current Time:", current_time)



seconds_str = current_datetime.strftime("%S")
print(seconds_str)