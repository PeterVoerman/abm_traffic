from mesa import Model
from mesa.space import Grid
import matplotlib.pyplot as plt

from agent import Car


class Road(Model):
    def __init__(self, length, n_cars, max_speed, n_lanes=1):
        super().__init__()

        self.length = length
        self.n_cars = n_cars
        self.max_speed = max_speed
        self.n_lanes = n_lanes

        self.n_agents = 0

        self.grid = Grid(self.length, self.n_lanes, False)

        print(self.grid.grid)

        self.init_cars()

        plt.xlim(0, length)
        plt.ylim(0, n_lanes)


    def add_car(self, pos=(0, 0)):
        self.n_agents += 1

        car = Car(self.n_agents, self, self.max_speed, 0, 0)

        self.grid.place_agent(car, pos)


    def remove_car(self, car):
        self.grid.remove_agent(car)

    
    def init_cars(self):
        for i in range(self.n_cars):
            self.add_car((i, 0))

    def draw(self):
        x_list = []
        y_list = []

        for x in range(self.length):
            for y in range(self.n_lanes):
                if self.grid.grid[x][y] != None:
                    x_list.append(x)
                    y_list.append(y)

        plt.scatter(x_list, y_list)
        plt.draw()
        plt.pause(0.001)
        plt.clf()



    def step(self, t):
        for car in self.grid:
            if car != None:
                car.step()

        for car in self.grid:
            if car != None:
                car.advance()

        if t % 5 == 0:
            self.add_car()

        self.draw()


    def run_model(self, step_count=1000):
        for t in range(step_count):
            self.step(t)


road = Road(100, 5, 10)

road.run_model()