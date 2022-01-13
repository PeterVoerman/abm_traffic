from mesa import Model
from mesa.space import Grid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

class Car():
    def __init__(self):
        super().__init__()

class Road(Model):
    def __init__(self, length, ncars):
        super().__init__()

        self.length = length
        self.ncars = ncars


        self.grid = Grid(self.length, 1, False)

        self.add_car()


    def add_car(self):
        car = Car()

        self.grid.place_agent(car, (0, 0))


    def remove_car(self, car):
        self.grid.remove_agent(car)


    def step(self, t):
        for car in self.grid:
            car.step()

        if t % 5 == 0:
            self.add_car()


    def run_model(self, step_count=1000):
        for t in range(step_count):
            self.step(t)
