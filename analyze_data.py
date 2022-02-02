import matplotlib.pyplot as plt

for speed in ['100', '110', '120']:
    with open(speed + 'kmh.csv', 'r') as data:
        # for braking_chance in [0, 0.5]:
        #     for n_cars in [200, 300, 400]:
        #         for sigma_pref_speed in [0.05, 0.15]:
        time_list = []
        speed_list = []

        counter = 0
        for line in data:
            if counter != 0:
                splitted = line.split(',')
                time_list.append(int(splitted[0]))
                speed_list.append(float(splitted[1]))
            
            counter += 1
        
        # plt.title(f"braking_chance: {braking_chance}, n_cars: {n_cars}, sigma_pref_speed: {sigma_pref_speed}")
        plt.plot(time_list, speed_list, label=speed + " kmh")

        time_list = []
        speed_list = []

plt.legend()
plt.show()