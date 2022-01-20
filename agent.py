from mesa.space import MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation, SimultaneousActivation

from mesa.datacollection import DataCollector

class Car(Agent):

	def __init__(self, unique_id, model, pref_speed=100, init_speed=0, risk=1, preferred_gap=1, init_lane=0):
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
		self.speed_change = 0

	def check_environment(self):
		"""Checks whether there are cars in the immediate neighborhood"""

		preferred_distance = self.speed * self.preferred_gap

		# cars that are preferred distance in front and in the next lane have
		# this distance. Therefore it is the taken radius for neighbor detection
		neighbors = self.model.space.get_neighbors(self.pos, (1 + preferred_distance ** 2), include_center = False)
		
		for neighbor in neighbors:
			# positive distance means this car is in front of its neighbor
			distance = self.pos[0] - neighbor.pos[0]
			speed_difference = self.speed - neighbor.speed
			distance_after_step = distance + speed_difference * self.model.timestep
			
			# too close for preferred distance
			if abs(distance_after_step) < preferred_distance:
				# same lane				
				if self.pos[1] == neighbor.pos[1]:
					if distance_after_step > 0:
						print("car too close behind")
					else:
						print("car too close in front")

				# neighbor is 1 lane to the right
				if self.pos[1] - neighbor.pos[1] == 1:
					print("car too close on the right")
				if self.pos[1] - neighbor.pos[1] == -1:
					print("car too close on the left")

	# def check_environment(self):
   	# 	# depends on structure, if exits are present,
   	# 	# need to check for them earlier, requires e.g. circle around
   	# 	# car to be explored. Taking exits is generally preplanned,
   	# 	# require car to go to said exit? implementation depends on the needs of model
	# 	self.check_front(self.vision_range)
	# 	self.check_sides()
	# 	self.check_behind(self.vision_range)

	# def check_front(self):
   	# 	# x amount of spaces in front
	# 	for i in self.vision_range:
	# 	# Check for cars in range, if too close (depends on self.risk), take action
	# 	# e.g. speed down : self.speed--
	# 		to_check = (self.pos[0] + i, self.lane)
	# 		if not self.model.out_of_bounds(to_check):
	# 			cell = self.get_cell_contents([to_check])
	# 			# if cell non-empty, car is present
	# 			if cell:
	# 				self.speed_change = (self.speed - cell[0].speed)/i


	# 		pass

	# def check_sides(self, vision_range):
	# 	# Left
	# 	#check_left (x amount of spaces again) for cars
	# 	if self.lane != self.model.nlanes - 1:
	# 		for i in self.vision_range - 1:
	# 			to_check = (self.pos[0] + i, self.lane + 1)
	# 			if not self.model.out_of_bounds(to_check):
	# 				cell = self.get_cell_contents([to_check])
	# 				# if cell non-empty, car is present
	# 				if cell:
	# 					self.allow_left = False
	# 				else:
	# 					self.allow_left = True
	# 	# Right
	# 	#check_right for cars
	# 	# If no cars, allow change of lane (if not out of bounds)
	# 	if self.lane != 1:
	# 		for i in self.vision_range - 1:
	# 			to_check = (self.pos[0] + i, self.lane - 1)
	# 			if not self.model.out_of_bounds(to_check):
	# 				cell = self.get_cell_contents([to_check])
	# 				# if cell non-empty, car is present
	# 				if cell:
	# 					self.allow_right = False
	# 				else:
	# 					self.allow_right = True

	# def check_behind(self, vision_range):
	# # x amount of spaces behind
	# 	for dist in vision_range:
	# 	# Check for cars in range, if too close (depends on self.risk), take action
	# 	# e.g. speed up : self.speed++
	# 		pass

	def step(self):
		self.check_environment()
		pass
	#self.new_position = new

	def advance(self):
		pass
	#self.move(self.new_position)