from mesa import Model
from mesa.space import ContinuousSpace
import matplotlib.pyplot as plt
import numpy as np

from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

from agent import Car
import random
import time


def get_avg_speed(model):
    speeds = [a.speed for a in model.schedule.agents]
    return np.mean(speeds)

def get_slow_cars(model):
    slow_cars = 0
    for car in model.schedule.agents:
        if car.speed < car.pref_speed:
            slow_cars += 1

    return slow_cars / len(model.schedule.agents)

def get_min_speeds(model):

    speeds = [a.speed for a in model.schedule.agents]
    return min(speeds)


class Road(Model):
    def __init__(self, length=3000, n_cars=50, max_speed=100, timestep=1, step_count = 3000, start_measurement = 2000, n_lanes=3, sigma_pref_speed=0.15, braking_chance=0.5):
        super().__init__()

        self.length = length
        self.n_cars = n_cars
        self.max_speed = max_speed
        self.timestep = timestep
        self.step_count = step_count
        self.start_measurement = start_measurement
        self.n_lanes = n_lanes
        self.braking_chance = braking_chance
        self.sigma_pref_speed = sigma_pref_speed

        self.n_agents = 0
        self.slow_car_list = []

        self.space = ContinuousSpace(self.length, self.n_lanes, True)
        self.schedule = SimultaneousActivation(self)

        self.datacollector = DataCollector(
            model_reporters={
                "Speeds": get_avg_speed,
                "Slow_cars": get_slow_cars,
                "Min_speed":get_min_speeds,
            },
            agent_reporters={"Speed": lambda agent: agent.speed},
            )
        
        self.init_model()


    def add_car(self, pos=(0, 0)):
        self.n_agents += 1

        pref_speed = np.random.normal(self.max_speed, (self.sigma_pref_speed * self.max_speed) / 3.6)
        switching_chance = np.random.normal(0.1, 0.05)

        car = Car(self.n_agents, self, pref_speed, init_speed=pref_speed, braking_chance=self.braking_chance, init_pos=pos, switching_chance=switching_chance)

        self.space.place_agent(car, car.pos)
        self.schedule.add(car)

    def remove_car(self, car):
        self.n_agents -= 1

        self.space.remove_agent(car)
        self.schedule.remove(car)

    def init_cars(self):
        for i in range(self.n_cars):
            self.add_car((i, 0))

    def draw(self):
        x_list = []
        y_list = []

        cars = self.schedule.agents
        color_list = []

        for car in cars:
            x_list.append(car.pos[0])
            y_list.append(car.pos[1])
            if car.speed < 1:
                color_list.append("red")
            elif car.speed > car.pref_speed - 1:
                color_list.append("green")
            else:
                color_list.append("orange")

        plt.xlim(0, self.length)
        plt.ylim(-0.5, self.n_lanes - 0.5)
        plt.scatter(x_list, y_list, c=color_list)

        plt.draw()
        plt.pause(0.001)
        plt.clf()

    def get_stats(self):
        slow_cars = 0
        for car in self.space._index_to_agent.values():
            if car.speed < car.pref_speed:
                slow_cars += 1

        self.slow_car_list.append(slow_cars)

    def plot_slow_cars(self):
        plt.plot(range(self.step_count), self.slow_car_list)
        plt.show()

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def init_model(self):
        # initialize the desired number of cars
        for i in range(self.n_cars):
            random_x = random.randint(0, self.length)
            random_lane = random.randint(0, self.n_lanes - 1)
            self.add_car((random_x, random_lane))

        for t in range(self.start_measurement):
            self.schedule.step()

# if __name__ == "__main__":

#     road = Road(100, 5, 10, 1)

#     road.run_model(animate=True)
#     road.plot_slow_cars()
start = time.time()
road = Road(3000, 100, 100/3.6, 0.1, 3000, 0, 3)
print(f"Time spent: {time.time() - start}")
# road.run_model(animate=True)
road.run_model2(animate=False)
print(f"Time spent: {time.time() - start}")