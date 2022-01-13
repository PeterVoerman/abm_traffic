from mesa import Model
from mesa.space import Grid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

class Car():
    def __init__(self):
        super().__init__()


class Road(Model):
    def __init__(self, length, ncars, max_speed, nlanes=1):
        super().__init__()

        self.length = length
        self.ncars = ncars
        self.max_speed = max_speed


        self.grid = Grid(self.length, nlanes, False)

        self.init_cars()


    def add_car(self, pos=(0, 0)):
        car = Car(self.max_speed)

        self.grid.place_agent(car, pos)


    def remove_car(self, car):
        self.grid.remove_agent(car)

    
    def init_cars(self):
        for i in range(self.ncars):
            self.add_car((i, 0))


    def step(self, t):
        for car in self.grid:
            car.step()

        if t % 5 == 0:
            self.add_car()


    def run_model(self, step_count=1000):
        for t in range(step_count):
            self.step(t)
