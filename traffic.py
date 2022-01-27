# Peter Voerman
# 11749547
# traffic.py
# Simulates traffic moving around a circle

import random
import matplotlib.pyplot as plt
import math
import numpy as np

plt.show()

# Simulates traffic moving around a circle
def traffic(amount_cars, amount_zones, max_speed, animation):
    total_speed = 0
    probability_list = []

    # Initializes the lists containing information about the cars
    if animation == True:
        speed_list = [max_speed] * amount_cars
        amount_steps = 501
    else:
        speed_list = [max_speed] * amount_cars
        amount_steps = 100

    position_list = []
    circle_x = [0] * amount_cars
    circle_y = [0] * amount_cars

    for i in range(amount_cars):
        position_list.append(i * amount_zones / amount_cars)
        probability = 0.75 * random.random()
        probability_list.append(probability)

    # Simulates the traffic
    for i in range(amount_steps):
        for j in range(amount_cars):

            # The car speeds up if it's allowed
            if speed_list[j] < max_speed:
                speed_list[j] += 1

            # Checks if the car is too close to the car in front of it
            distance = position_list[(j + 1) % (amount_cars)] - position_list[j]
            if distance < 0:
                distance += amount_zones

            if speed_list[j] >= distance:
                speed_list[j] = distance - 1

            # Slows the car down randomly
            if speed_list[j] > 0:
                if random.random() < probability_list[j]:
                    speed_list[j] -= 1

            total_speed += speed_list[j]

        # Gives the cars their new position in radial coordinates
        for j in range(amount_cars):
            position_list[j] = (position_list[j] + speed_list[j]) % amount_zones
            angle = 2 * math.pi * position_list[j] / amount_zones
            circle_x[j] = math.cos(angle)
            circle_y[j] = math.sin(angle)

        # Animates the cars moving around the track
        if animation == True:
            plt.axis('square')
            plt.text(0, 0, "Time = %d" %i)
            plt.xlim(-1.1, 1.1)
            plt.ylim(-1.1, 1.1)
            plt.plot(circle_x, circle_y, 'o', markersize = 4)
            plt.draw()
            plt.pause(0.01)
            plt.clf()

    # Calculates the average speed of the cars
    average_speed = total_speed / (amount_cars * amount_steps)

    # Makes sure the figure doesn's disappear after the animation is done
    if animation == True:
        plt.show()

    return average_speed, circle_x, circle_y

# Calculates the average speed for different amounts of cars and maximum speeds
def traffic_test(amount_cars, amount_zones, max_speed):
    av_speed_list = []
    car_list = []

    # Loops through different amounts of cars
    for i in np.arange(2, amount_cars + 1):
        total = 0

        # Calculates the average of five simulations
        for j in range(5):
            total += 3.6 * traffic(i, amount_zones, int(max_speed // 3.6), False)[0]
        av_speed_list.append(total / 5)
        car_list.append(1000 * i / amount_zones)
    
    return car_list, av_speed_list

# Animates fifty cars moving around a track
traffic(50, 1000, int(100/3.6), True)[0]

# Plots the average speed for different maximum speeds and car densities
plt.title("The average speed of the cars for different maximum speeds and car densities")
plt.xlabel("Cars per km")
plt.ylabel("Average speed (km/h)")
car_25, av_speed_25 = traffic_test(50, 1000, 50)
car_100, av_speed_100 = traffic_test(50, 1000, 100)
car_500, av_speed_500 = traffic_test(50, 1000, 200)
car_1000, av_speed_1000 = traffic_test(50, 1000, 400)
plt.plot(car_25, av_speed_25, label="Max speed = 50 km/h")
plt.plot(car_100, av_speed_100, label="Max speed = 100 km/h")
plt.plot(car_500, av_speed_500, label="Max speed = 200 km/h")
plt.plot(car_1000, av_speed_1000, label="Max speed = 400 km/h")
plt.legend()
plt.show()
