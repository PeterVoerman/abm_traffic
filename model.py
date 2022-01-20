from mesa import Model
from mesa.space import ContinuousSpace
import matplotlib.pyplot as plt

from agent import Car


class Road(Model):
    def __init__(self, length, n_cars, max_speed, timestep, n_lanes=1):
        super().__init__()

        self.length = length
        self.n_cars = n_cars
        self.max_speed = max_speed
        self.timestep = timestep
        self.n_lanes = n_lanes

        self.n_agents = 0
        self.slow_car_list = []

        self.space = ContinuousSpace(self.length, self.n_lanes, False)

        self.init_cars()

        

    def add_car(self, pos=(0, 0)):
        self.n_agents += 1

        car = Car(self.n_agents, self, self.max_speed, 0, 0)

        self.space.place_agent(car, pos)


    def remove_car(self, car):
        self.space.remove_agent(car)

    
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
        for car in self.space._index_to_agent.values():
            car.step()

        for car in self.space._index_to_agent.values():
            car.advance()

        if t % 5 == 0:
            self.add_car()

        if self.animate:
            self.draw()
        self.get_stats()


    def run_model(self, step_count=1000, animate=True):
        self.animate = animate
        self.step_count = step_count
        for t in range(step_count):
            self.step(t)


road = Road(100, 5, 10, 1)

road.run_model(animate=True)
road.plot_slow_cars()