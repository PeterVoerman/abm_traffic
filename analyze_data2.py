import matplotlib.pyplot as plt

"""PART 1: read in data"""

time_list = []
speed_list = []

first = True
with open('data.csv', 'r') as data:
    for line in data:
        if not first:
            splitted = line.split(',')
            time_list.append(int(splitted[0]))
            speed_list.append(float(splitted[1]))
        else:
            first = False

"""PART 2: store data grouped by parameter set"""

def params_to_key(speed, braking_chance, n_cars, sigma_pref_speed):
    return "speed" + str(speed) + "_braking" + str(braking_chance) + "_ncars" + str(n_cars) + "_sigma" + str(sigma_pref_speed)

tracker = 0
time_dict = {}
speed_dict = {}

for speed in [100, 110, 120, 130]:
    for braking_chance in [0, 0.5]:
        for n_cars in [200, 300, 400]:
            for sigma_pref_speed in [0.05, 0.15]:            
                time_slice = time_list[tracker:tracker + n_cars]
                speed_slice = speed_list[tracker:tracker + n_cars]
                tracker += n_cars

                key = params_to_key(speed, braking_chance, n_cars, sigma_pref_speed)
                print(key)
                time_dict[key] = time_slice
                speed_dict[key] = speed_slice

            #     plt.title(f"braking_chance: {braking_chance}, n_cars: {n_cars}, sigma_pref_speed: {sigma_pref_speed}")
            #     plt.plot(time_list, speed_list, label=speed + " kmh")
            
            # plt.legend()
            # plt.show()

"""STEP 3: Analyze data"""
