from mesa import Model
from mesa.space import ContinuousSpace
import matplotlib.pyplot as plt
import numpy as np

from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

from agent import Car
import numpy as np
import pandas as pd
import random

from itertools import product

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
    def __init__(self, length=3000, n_cars=50, max_speed=100, timestep=1, step_count=2500, start_measurement=500, n_lanes=3, sigma_pref_speed=0.15, braking_chance=0.5):

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
                "Min_speed": get_min_speeds,
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

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    def init_model(self):
        # initialize the desired number of cars
        l = list(product(range(0, self.length), range(0, self.n_lanes)))
        for i in range(self.n_cars):
            random_pos = l.pop(random.randrange(len(l)))
            self.add_car(pos=tuple(random_pos))


        # for i in range(self.n_cars):
        #     random_x = random.randint(0, self.length)
        #     random_lane = random.randint(0, self.n_lanes - 1)
        #     self.add_car(pos=(random_x, random_lane))

        for t in range(self.start_measurement):
            self.schedule.step()
        
        # reset distance to 0 so that the measurement can begin
        for car in self.space._index_to_agent.values():
            car.distance = 0
        
# parameter lists for each parameter to be tested in batch run
# br_params = {
#     "max_speed": [100, 120, 130],
#     "braking_chance": [0, 0.25, 0.5],
#     "spawn_chance": [1/5, 1/4, 1/3],
#     "sigma_pref_speed": [0.05, 0.15],

# }

br_params = {
    "max_speed": [100],
    "braking_chance": [0.5],
    "n_cars": [400],
    "sigma_pref_speed": [0.15],

}

br = BatchRunner(
    Road,
    br_params,
    iterations=1,
    max_steps=2500,
    model_reporters={"Data Collector": lambda m: m.datacollector},
)

if __name__ == "__main__":
    br.run_all()
    br_df = br.get_model_vars_dataframe()
    br_step_data = pd.DataFrame()
    for i in range(len(br_df["Data Collector"])):
        if isinstance(br_df["Data Collector"][i], DataCollector):
            i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
            br_step_data = br_step_data.append(i_run_data, ignore_index=True)
    br_step_data.to_csv("test.csv")
