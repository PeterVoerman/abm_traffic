from mesa import Model
from mesa.space import ContinuousSpace
import matplotlib.pyplot as plt
import numpy as np

from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

from agent import Car
import numpy as np


def get_avg_speed(model):
    speeds = [a.speed for a in model.schedule.agents]
    return np.mean(speeds)

def get_slow_cars(model):
    slow_cars = 0
    for car in model.schedule.agents:
        if car.speed < car.pref_speed:
            slow_cars += 1

    return slow_cars


class Road(Model):
    def __init__(self, length=100, n_cars=50, max_speed=100, timestep=1, n_lanes=1):
        super().__init__()

        self.length = length
        self.n_cars = n_cars
        self.max_speed = max_speed
        self.timestep = timestep
        self.n_lanes = n_lanes

        self.n_agents = 0
        self.slow_car_list = []

        self.space = ContinuousSpace(self.length, self.n_lanes, False)
        self.schedule = SimultaneousActivation(self)
        self.init_cars()

        self.datacollector = DataCollector(
            model_reporters={
                "Speeds": get_avg_speed,
                "Slow cars": get_slow_cars,
            },
            agent_reporters={"Speed": lambda agent: agent.speed},
            )

        self.datacollector.collect(self)


    def add_car(self, pos=(0, 0)):
        self.n_agents += 1

        pref_speed = np.random.normal(self.max_speed, 5 / 3.6)

        car = Car(self.n_agents, self, pref_speed, 0, 0)

        self.space.place_agent(car, pos)
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

        cars = self.space._index_to_agent.values()

        for car in cars:
            x_list.append(car.pos[0])
            y_list.append(car.pos[1])

        plt.xlim(0, self.length)
        plt.ylim(-0.5, self.n_lanes - 0.5)
        plt.scatter(x_list, y_list)
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

        if t % 1 == 0:
            self.add_car()

        if self.animate:
            self.draw()
        self.get_stats()
        self.datacollector.collect(self)
        # Dit werkt ook om de huidige positie te krijgen
        # frame = get_agent_vars_dataframe()
        # pos = frame["pos"]


    def run_model(self, step_count=1000, animate=True):
        self.animate = animate
        self.step_count = step_count
        for t in range(step_count):
            self.step(t)


# if __name__ == "__main__":

#     road = Road(100, 5, 10, 1)

#     road.run_model(animate=True)
#     road.plot_slow_cars()

road = Road(10000, 5, 100/3.6, 1, 2)

road.run_model(animate=False)
road.plot_slow_cars()
