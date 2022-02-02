import matplotlib.pyplot as plt

"""PART 1: read in data"""

actual_speeds = []
pref_speeds = []

first = True
with open('data.csv', 'r') as data:
    for line in data:
        if not first:
            splitted = line.split(',')
            actual_speeds.append(int(splitted[0]))
            pref_speeds.append(float(splitted[1]))
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

"""STEP 3: Analyze data"""
