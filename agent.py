from mesa.space import MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation, SimultaneousActivation

from mesa.datacollection import DataCollector

import numpy as np

class Car(Agent):

	def __init__(self, unique_id, model, pref_speed=100, init_speed=0, risk=1, preferred_gap=1, init_lane=0, acceleration=5, deceleration=-7, braking_chance=0.5, truck = False):
		"""
		Creates a new battery with potential for battery recharge time.

		preferred gap is in seconds
		"""
		super().__init__(unique_id, model)
		self.speed = init_speed
		self.allow_left = False
		self.allow_right = False
		self.pref_speed = pref_speed
		self.risk = risk
		self.preferred_gap = preferred_gap
		self.pos = (0, init_lane)
		self.acceleration = acceleration
		self.deceleration = deceleration
		self.braking_chance = braking_chance
		self.truck = truck

	def accelerate(self):
		self.speed += self.acceleration * self.model.timestep

		# cap at pref_speed
		if self.speed > self.pref_speed:
			self.speed = self.pref_speed

	def brake(self):
		self.speed += self.deceleration * self.model.timestep

		# cap at pref_speed
		if self.speed < 0:
			self.speed = 0

	def switch_lane(self, direction):
		if direction == 'L':
			self.new_pos[1] = self.new_pos[1] + 1
		elif direction == 'R':
			self.new_pos[1] = self.new_pos[1] - 1

	def move_forward(self):
		self.new_pos[0] += self.speed * self.model.timestep

	def check_environment(self):
		"""Checks whether there are cars in the immediate neighborhood"""

		# start on true and set to False if other cars are found
		self.space_ahead = True
		self.space_left = self.pos[1] != self.model.n_lanes - 1
		self.space_right = self.pos[1] != 0

		preferred_distance = self.speed * self.preferred_gap

		# cars that are preferred distance in front and in the next lane have
		# this distance. Therefore it is the taken radius for neighbor detection
		neighbors = self.model.space.get_neighbors(self.pos, (1 + preferred_distance ** 2) ** (1 / 2), include_center = False)
		
		for neighbor in neighbors:
			# positive distance means this car is in front of its neighbor
			distance = self.pos[0] - neighbor.pos[0]
			speed_difference = self.speed - neighbor.speed
			distance_after_step = distance + speed_difference * self.model.timestep
			
			# too close for preferred distance
			if abs(distance_after_step) < preferred_distance:
				# same lane				
				if self.pos[1] == neighbor.pos[1]:
					if distance_after_step < 0:
						self.space_ahead = False

				# neighbor is 1 lane to the right
				if self.pos[1] - neighbor.pos[1] == 1 or self.pos[1] == 0:
					self.space_right = False
				if self.pos[1] - neighbor.pos[1] == -1:
					self.space_left = False

	def step(self):
		self.new_pos = list(self.pos)

		if self.speed < self.pref_speed:
			self.accelerate()

		self.check_environment()

		if self.space_ahead:
			if self.space_right:
				self.switch_lane('R')
		else:
			# note: maybe implement chance
			if self.space_left and not self.truck:
				self.switch_lane('L')

			else:
				# note: maybe implement adaptive braking
				self.brake()

		if np.random.random() < self.braking_chance:
			self.brake()
		
		self.move_forward()

	def advance(self):
		if self.new_pos[0] > self.model.length:
			self.model.schedule.remove(self)
			self.model.space.remove_agent(self)

			return

		self.model.space.move_agent(self, tuple(self.new_pos))

		