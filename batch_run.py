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

def get_avg_speed(model):
    if len(model.schedule.agents) == 0:
        return 0
    speeds = [a.speed for a in model.schedule.agents]
    return np.mean(speeds)

def get_slow_cars(model):
    if len(model.schedule.agents) == 0:
        return 0
    slow_cars = 0
    for car in model.schedule.agents:
        if car.speed < car.pref_speed:
            slow_cars += 1

    return slow_cars / len(model.schedule.agents)

def get_min_speeds(model):
    if len(model.schedule.agents) == 0:
        return 0
    speeds = [a.speed for a in model.schedule.agents]
    return min(speeds)



class Road(Model):
    def __init__(self, length=10000, max_speed=100, timestep=1, n_lanes=1, spawn_chance=1/5, sigma_pref_speed=0.15, braking_chance=0):
        super().__init__()

        self.length = length

        self.max_speed = max_speed
        self.timestep = timestep
        self.n_lanes = n_lanes
        self.spawn_chance = spawn_chance
        self.sigma_pref_speed = sigma_pref_speed
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


    def add_car(self, pos=(0, 0)):
        self.n_agents += 1

        lane = np.random.randint(0, self.n_lanes)

        pref_speed = np.random.normal(self.max_speed, (self.sigma_pref_speed * self.max_speed) / 3.6)

        car = Car(self.n_agents, self, pref_speed, pref_speed, init_lane=lane, braking_chance=self.braking_chance, switching_chance=0.1)

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
            if car.speed < car.pref_speed:
                color_list.append("red")
            elif car.speed > car.pref_speed:
                color_list.append("purple")
            else:
                color_list.append("green")

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

        # if t % 10 == 0:
        #     self.add_car()

        if np.random.random() > self.spawn_chance:
            self.add_car()

        # if self.animate and self.step_count % 10 == 0:
        #     self.draw()

        # self.step_count -= 1
        self.datacollector.collect(self)


    def run_model(self, step_count=10000, animate=True):
        self.animate = animate
        self.step_count = step_count
        self.step()

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

# parameter lists for each parameter to be tested in batch run
# br_params = {
#     "max_speed": [100, 120, 130],
#     "braking_chance": [0, 0.25, 0.5],
#     "spawn_chance": [1/5, 1/4, 1/3],
#     "sigma_pref_speed": [0.05, 0.15],

# }

br_params = {
    "max_speed": [100],
    "braking_chance": [0, 0.5],
    "spawn_chance": [1/5, 1/3],
    "sigma_pref_speed": [0.05, 0.15],

}

br = BatchRunner(
    Road,
    br_params,
    iterations=1,
    max_steps=1000,
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
    br_step_data.to_csv("batch.csv")
