from typing import List, Tuple
import numpy as np


class Characteristic:
	"""
	Class representing a single characteristic present on a fuzzy logic axis, looking like:

							LEE   ______________ RES
								 /				\
								/				 \
							   /				  \
	_______________________LES/					   \REE___________________________________
	-------------------------------------------------------------------------------------> x

	Arguments:
		name - characteristic identifier

		left_edge_start - x where left edge starts
		left_edge_end - x where left edge ends

		right_edge_start - x where right edge starts
		right_edge_end - x where right edge ends
	"""
	def __init__(self, name: str,
					   left_edge_start: int,
				 	   right_edge_start: int,
				 	   left_edge_end: int,
				 	   right_edge_end: int):

		# neccessary arguments
		self.name = name
		self.left_edge_start = left_edge_start
		self.right_edge_start = right_edge_start
		self.left_edge_end = left_edge_end
		self.right_edge_end = right_edge_end

		# calculate 1st degree polynomials
		self.left_edge_slope = self.GetSlope(side='left')
		self.right_edge_slope = self.GetSlope(side='right')


	def GetValue(self, x: float) -> float:
		"""
		Return the value of characteristic it takes for given x on x_axis.
		"""
		# if on left or right of characteristic
		if x <= self.left_edge_start or x >= self.right_edge_end:
			return 0

		# if on left slope
		if x >= self.left_edge_start and x <= self.left_edge_end:
			return self.left_edge_slope[0]*x + self.left_edge_slope[1]

		# if in the middle
		if x >= self.left_edge_end and x <= self.right_edge_start:
			return 1

		# if on right slope
		if x >= self.right_edge_start and x <= self.right_edge_end:
			return self.right_edge_slope[0]*x + self.right_edge_slope[1]


	def GetSlope(self, side: str) -> tuple[float]:
		"""
		Calculate first degree polynomial fit to two points.

		Arguments:
			side - either 'left' or 'right', depending on which slope it is

		Returns:
			(a, b) as in y = a*x + b
		"""
		# left slope
		if side == 'left':

			a, b = np.polyfit(x=[self.left_edge_start, self.left_edge_end],
							  y=[0, 1],
							  deg=1)

		# right slope
		if side == 'right':

			# fit a 1-degree polynomial to two points
			a, b = np.polyfit(x=[self.right_edge_start, self.right_edge_end],
							  y=[1, 0],
							  deg=1)
		
		return (a, b)


class FuzzyAxis:
	"""
	Class representing a single fuzzy axis with multiple characteristics on it.
	"""
	def __init__(self, name: str, characteristics: List[Characteristic]):
		self.name = name
		self.characteristics = characteristics


	def GetCharacteristicsValues(self, value: float) -> dict:
		"""
		Get value for each characteristic present on FuzzyAxis.
		"""
		output_values = {}
		for characteristic in self.characteristics:
			output_values[characteristic.name] = characteristic.GetValue(value)

		return output_values

def initialize_axes():
	axes = []

	# -----------------------------PENDULUM ANGLE-----------------------------
	PendulumTiltedLeft = Characteristic(name="PendulumTiltedLeft",
										left_edge_start=-0.05,
										left_edge_end=0.1,
										right_edge_start=100,
										right_edge_end=101)

	PendulumTiltedRight = Characteristic(name="PendulumTiltedRight",
										 left_edge_start=-101,
										 left_edge_end=-100,
										 right_edge_start=-0.1,
										 right_edge_end=0.05)

	PendulumCentered = Characteristic(name="PendulumCentered",
									  left_edge_start=-0.1,
									  left_edge_end=0,
									  right_edge_start=0,
									  right_edge_end=0.1)

	PendulumAngleAxis = FuzzyAxis(name="PendulumAngleAxis",
								  characteristics=[PendulumTiltedRight, PendulumTiltedLeft, PendulumCentered])
	axes.append(PendulumAngleAxis)

	# -----------------------------PENDULUM ANGLE DERIVATIVE-----------------------------
	PendulumRotatingLeft = Characteristic(name="PendulumRotatingLeft",
										  left_edge_start=-0.2,
										  left_edge_end=0.05,
										  right_edge_start=100,
										  right_edge_end=101)

	PendulumRotatingRight = Characteristic(name="PendulumRotatingRight",
										   left_edge_start=-101,
										   left_edge_end=-100,
										   right_edge_start=-0.05,
										   right_edge_end=0.2)

	PendulumRotationAxis = FuzzyAxis(name="PendulumRotationAxis",
									 characteristics=[PendulumRotatingLeft, PendulumRotatingRight])
	axes.append(PendulumRotationAxis)

	# -----------------------------CART POSITION-----------------------------
	CartOnLeft = Characteristic(name="CartOnLeft",
								left_edge_start=-101,
								left_edge_end=-100,
								right_edge_start=-35,
								right_edge_end=20)

	CartOnRight = Characteristic(name="CartOnRight",
								 left_edge_start=-20,
								 left_edge_end=35,
								 right_edge_start=100,
								 right_edge_end=101)

	CartPositionAxis = FuzzyAxis(name="CartPositionAxis",
								 characteristics=[CartOnRight, CartOnLeft])

	axes.append(CartPositionAxis)

	return axes
