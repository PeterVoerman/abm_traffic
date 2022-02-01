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
    def __init__(self, length=100, n_cars=50, max_speed=100, timestep=1, step_count = 10000, n_lanes=1, braking_chance=0.5):
        super().__init__()

        self.length = length
        self.n_cars = n_cars
        self.max_speed = max_speed
        self.timestep = timestep
        self.step_count = step_count
        self.n_lanes = n_lanes
        self.braking_chance = braking_chance

        self.n_agents = 0
        self.slow_car_list = []

        self.space = ContinuousSpace(self.length, self.n_lanes, False)
        self.schedule = SimultaneousActivation(self)

        self.datacollector = DataCollector(
            model_reporters={
                "Speeds": get_avg_speed,
                "Slow_cars": get_slow_cars,
                "Min_speed":get_min_speeds,
            },
            agent_reporters={"Speed": lambda agent: agent.speed},
            )

        #self.datacollector.collect(self)


    def add_car(self, truck = False, pos=(0, 0)):
        self.n_agents += 1

        if truck:
            pref_speed = np.random.normal(90 / 3.6, 2 / 3.6)
            switching_chance = 0
            lane = 0
        else:
            pref_speed = np.random.normal(self.max_speed, 15 / 3.6)
            switching_chance = np.random.normal(0.1, 0.05)
            lane = np.random.randint(0, self.n_lanes)

        car = Car(self.n_agents, self, pref_speed, pref_speed, init_speed=pref_speed, braking_chance=self.braking_chance, init_lane=lane, switching_change=switching_chance)

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

        # print([car.speed for car in cars])
        for car in cars:
            x_list.append(car.pos[0])
            y_list.append(car.pos[1])
            if car.truck:
                color_list.append("blue")
            elif car.speed < 1:
                color_list.append("red")
            elif car.speed > car.pref_speed - 1:
                color_list.append("green")
            else:
                color_list.append("orange")

        plt.xlim(0, self.length)
        plt.ylim(-0.5, self.n_lanes - 0.5)
        plt.scatter(x_list, y_list, c=color_list)

        # speeds = [a.speed for a in self.schedule.agents]
        # plt.hist(speeds, bins = range(0, 30, 1))
        # plt.ylim(0, 70)

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

    def step(self, t):
        # for car in self.space._index_to_agent.values():
        #     car.step()

        # Set every car ready for a move, move when every move is decided.

        # for car in self.space._index_to_agent.values():
        #     car.advance()
        self.schedule.step()

        if t % 3 == 0:
            # spawn a truck with a 0.05% probability
            if random.random() < 0.05:
                self.add_car(truck=True)
            else:
                self.add_car()
            # self.add_car((0, 1))
            # self.add_car((500, 0))
            # self.add_car((500, 1))

        if self.animate and t % 10 == 0:
            self.draw()

        self.datacollector.collect(self)


    def run_model(self, animate=True):
        self.animate = animate
        for t in range(self.step_count):
            print(f"Step {t+1}/{self.step_count}", end='\r')
            self.step(t)

        # all model reporters of the datacollector
        df_model = self.datacollector.get_model_vars_dataframe()
        # all agent reporters of the datacollector
        df_agents = self.datacollector.get_agent_vars_dataframe()

        # resulting dataframes
        # print(df_model)
        # print(df_agents)

        plt.plot(range(0, len(df_model)), df_model['Slow_cars'])
        plt.show()

        plt.plot(range(0, len(df_model)), df_model['Speeds'])
        plt.show()

        plt.plot(range(0, len(df_model)), df_model['Min_speed'])
        plt.show()

        # example of agent variables (currently only speed) at final index
        # print(df_agents.loc[100])

        # example of model reporter category
        # print(df_model["Slow_cars"])

# if __name__ == "__main__":

#     road = Road(100, 5, 10, 1)

#     road.run_model(animate=True)
#     road.plot_slow_cars()

road = Road(3000, 5, 120/3.6, 0.1, 1000, 3)
road.run_model(animate=False)