import matplotlib.pyplot as plt
import numpy as np

"""PART 1: read in data"""

actual_speeds = []
pref_speeds = []

first = True
with open('test2.csv', 'r') as data:
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

for speed in [100, 110, 120, 130]:
    for braking_chance in [0, 0.5]:
        for n_cars in [200, 300, 400]:
            for sigma_pref_speed in [0.05, 0.15]:
                actual_speeds_slice = actual_speeds[tracker:tracker + n_cars]
                pref_speeds_slice = pref_speeds[tracker:tracker + n_cars]
                tracker += n_cars

                key = params_to_key(speed, braking_chance, n_cars, sigma_pref_speed)
                # print(key)
                actual_speeds_dict[key] = actual_speeds_slice
                pref_speeds_dict[key] = pref_speeds_slice

                # print(actual_speeds_slice[0:10])
                # print(pref_speeds_slice[0:10])

"""STEP 3: Analyze data"""
# for braking_chance in [0, 0.5]:
#     for n_cars in [200, 300, 400]:
#         for sigma_pref_speed in [0.05, 0.15]:
#             for speed in [100, 110, 120, 130]:
#                 key = params_to_key(speed, braking_chance, n_cars, sigma_pref_speed)

#                 actual_speeds_slice = actual_speeds_dict[key]
#                 pref_speeds_slice = pref_speeds_dict[key]

#                 ratio = [actual_speeds_slice[i] / pref_speeds_slice[i] for i in range(len(actual_speeds_slice))]

#                 plt.xlim(0, 1)
#                 plt.title(key)
#                 plt.hist(ratio, bins=np.arange(0, 1, 0.05))
#                 plt.show()

fig, ax = plt.subplots()

colors = [(0, 0, 1, 0.25), (0, 1, 0, 0.25), (1, 0, 0, 0.25), (1, 1, 0, 0.25)]

speeds = [100, 110, 120, 130]
braking_chances = [0, 0.5]
n_carss = [200, 300, 400]
sigma_pref_speeds = [0.05, 0.15]

# dict = {100: (1, 1, 0, 0.25), 110: (0, 1, 0, 0.25), 120: (0, 0, 1, 0.25), 130: (1, 0, 0, 0.25)}

index = 0

for sigma_pref_speed in sigma_pref_speeds:
    total_list = []
    for braking_chance in braking_chances:
        for speed in speeds:
            for n_cars in n_carss:
                key = params_to_key(speed, braking_chance, n_cars, sigma_pref_speed)

                actual_speeds_slice = actual_speeds_dict[key]
                total_list += actual_speeds_slice
    
    ax.hist(total_list, bins=range(0, 100, 5), label=f"variation: {sigma_pref_speed}", histtype='step', stacked=False, fill=True, fc=colors[index])
    index += 1

ax.set_xlim(0, 100)
ax.set_title("Speed distribution for ")
ax.legend()
plt.show()