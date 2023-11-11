import datetime
import numpy as np

current_datetime = datetime.datetime.now()
current_time_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
print("Current Date and Time:", current_datetime)
current_time = current_datetime.time()
print("Current Time:", current_time)



seconds_str = current_datetime.strftime("%S")
print(seconds_str)

θ=np.array([[-0.80095251],
                    [-0.17539073],
                    [-1.18726351],
                    [-1.20933487],
                    [-0.40805846],
                    [ 1.88959092]])
Amax = 20
Aavg = Amax*0.75
for i in range(6):
    Vmax = np.sqrt(abs(θ[i,0]) * Amax/2)
    print(Vmax)