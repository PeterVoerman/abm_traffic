import matplotlib.pyplot as plt
import numpy as np

"""PART 1: read in data"""

actual_speeds = []
pref_speeds = []

first = True
with open('car_average.csv', 'r') as data:
    for line in data:
        if not first:
            splitted = line.split(',')

            actual_speeds.append(float(splitted[1]) / 2000)
            pref_speeds.append(float(splitted[2]))
        else:
            first = False

"""PART 2: store data grouped by parameter set"""

def params_to_key(speed, braking_chance, n_cars, sigma_pref_speed):
    return "speed" + str(speed) + "_braking" + str(braking_chance) + "_ncars" + str(n_cars) + "_sigma" + str(sigma_pref_speed)

tracker = 0
actual_speeds_dict = {}
pref_speeds_dict = {}

speeds = [100, 110, 120, 130]
braking_chances = [0, 0.5]
n_carss = [100, 200, 300]
sigma_pref_speeds = [0.05, 0.15]

for speed in speeds:
    for braking_chance in braking_chances:
        for n_cars in n_carss:
            for sigma_pref_speed in sigma_pref_speeds:
                actual_speeds_slice = actual_speeds[tracker:tracker + n_cars]
                pref_speeds_slice = pref_speeds[tracker:tracker + n_cars]
                tracker += n_cars

                key = params_to_key(speed, braking_chance, n_cars, sigma_pref_speed)

                actual_speeds_dict[key] = actual_speeds_slice
                pref_speeds_dict[key] = pref_speeds_slice

"""STEP 3: Analyze data"""
fig, ax = plt.subplots()

colors = [(0, 0, 1, 0.25), (0, 1, 0, 0.25), (1, 0, 0, 0.25), (1, 1, 0, 0.25)]

index = 0

for speed in speeds:
    total_list = []
    for braking_chance in [0]:
        for sigma_pref_speed in sigma_pref_speeds:
            for n_cars in [100]:
                key = params_to_key(speed, braking_chance, n_cars, sigma_pref_speed)

                actual_speeds_slice = actual_speeds_dict[key]
                total_list += actual_speeds_slice
    
    ax.hist(total_list, bins=range(0, 130, 5), label=f"speed limit: {speed}km/h", histtype='step', stacked=False, fill=True, fc=colors[index])
    ax.vlines(sum(total_list) / len(total_list), 0, 150, color=colors[index][0:3])
    index += 1

ax.set_xlim(0, 130)
ax.set_ylim(0, 150)
ax.set_xlabel("Speed (km/h)")
ax.set_ylabel("Number of cars")
ax.set_title("Total speed distribution for 300 cars, no random braking")
ax.legend()
plt.show()