import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from SALib.sample import saltelli

from mesa import Model
from mesa.space import ContinuousSpace

from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

from agent import Car
import random

from mesa.batchrunner import BatchRunner
from SALib.analyze import sobol

from itertools import combinations, product

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
        self.n_cars = int(n_cars)
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
            agent_reporters={
                "distance": "distance",
                "pref_speed": "pref_speed"},
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

br_params = {
    "max_speed": [90, 95, 100, 105, 110, 115, 120, 125, 130],
    "braking_chance": [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
    "n_cars": [50, 75, 100, 125, 150, 175, 200, 225, 250],
    "sigma_pref_speed": [0, 0.05, 0.1, 0.15, 0.2, 0.25],
}


# Set the repetitions, the amount of steps, and the amount of distinct values per variable
replicates = 25
max_steps = 1000

# Set the outputs
model_reporters={"Avg Speed": lambda m: np.mean([a.speed for a in m.schedule.agents])}
    

data = {}

for param in br_params:

    batch = BatchRunner(Road, 
                        max_steps=max_steps,
                        iterations=replicates,
                        variable_parameters={param: br_params[param]},
                        model_reporters=model_reporters,
                        display_progress=True)
    
    batch.run_all()
    
    data[param] = batch.get_model_vars_dataframe()
    batch.get_model_vars_dataframe().to_csv(f"data/{param}.csv")

print(data)

def plot_param_var_conf(df, var, param, i):
    """
    Helper function for plot_all_vars. Plots the individual parameter vs
    variables passed.

    Args:
        ax: the axis to plot to
        df: dataframe that holds the data to be plotted
        var: variables to be taken from the dataframe
        param: which output variable to plot
    """
    x = df.groupby(var).mean().reset_index()[var]
    y = df.groupby(var).mean()[param]

    replicates = df.groupby(var)[param].count()
    err = (1.96 * df.groupby(var)[param].std()) / np.sqrt(replicates)

    plt.plot(x, y, c='k')
    plt.fill_between(x, y - err, y + err)

    plt.xlabel(var)
    plt.ylabel(param)
    plt.show()

def plot_all_vars(df, param):
    """
    Plots the parameters passed vs each of the output variables.

    Args:
        df: dataframe that holds all data
        param: the parameter to be plotted
    """

    #f, axs = plt.subplots(4, figsize=(7, 10))
    
    for i, var in enumerate(br_params):
        plot_param_var_conf(data[var], var, param, i)


#plot_all_vars(data, "Avg Speed")
