from mesa.space import MultiGrid
from mesa import Agent, Model
from mesa.time import RandomActivation, SimultaneousActivation

from mesa.datacollection import DataCollector

class Car(Agent):

	def __init__(self, unique_id, model, pref_speed, init_speed, risk):
		"""
		Creates a new battery with potential for battery recharge time.
		"""
		super().__init__(unique_id, model)
		self.speed = init_speed
		self.allow_lane_change = False
		self.pref_speed = pref_speed
		self.risk = risk
		self.vision_range = 1

	def check_environment(self):
   		# depends on structure, if exits are present,
   		# need to check for them earlier, requires e.g. circle around
   		# car to be explored. Taking exits is generally preplanned,
   		# require car to go to said exit? exit implementation is complicated
		self.check_front(self.vision_range)
		self.check_sides()
		self.check_behind(self.vision_range)

	def check_front(self, vision_range):
   		# x amount of spaces in front
		for dist in vision_range:
		# Check for cars in range, if too close (depends on self.risk), take action
		# e.g. speed down : self.speed--
			pass

	def check_sides(self, vision_range):
		# Left
		#check_left (x amount of spaces again) for cars
		# Right
		#check_right for cars
		# If no cars, allow change of lane (if not out of bounds)
		pass

	def check_behind(self, vision_range):
	# x amount of spaces behind
		for dist in vision_range:
		# Check for cars in range, if too close (depends on self.risk), take action
		# e.g. speed up : self.speed++
			pass

	def step(self):
		pass
	#self.new_position = new

	def advance(self):
		pass
	#self.move(self.new_position)