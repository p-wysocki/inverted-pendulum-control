from typing import List, Tuple
import numpy as np


class Characteristic:
	"""
	Class representing a single characteristic present on a fuzzy logic axis, looking like:

								  ______________
								 /				\
								/				 \
							   /				  \
	__________________________/					   \______________________________________
	-------------------------------------------------------------------------------------> x

	Arguments:
		name - characteristic identifier

		left_edge_start - x where left edge starts
		left_edge_end - x where left edge ends (optional, only if there is a left slope)

		right_edge_start - x where right edge starts
		right_edge_end - x where right edge ends (optional, only if there is a right slope)
	"""
	def __init__(self, name: str,
					   left_edge_start: int,
				 	   right_edge_start: int,
				 	   left_edge_end: int = None,
				 	   right_edge_end: int = None):

		# neccessary arguments
		self.name = name
		self.left_edge_start = left_edge_start
		self.right_edge_start = right_edge_start
		
		# optional arguments
		self.left_edge_end = left_edge_end
		self.right_edge_end = right_edge_end

		# calculate 1st degree polynomials
		self.left_edge_slope = self.GetSlope(side='left')
		self.right_edge_slope = self.GetSlope(side='right')


	def GetValue(self, x) -> float:

		# if left side is continous 1
		if not self.left_edge_end and x <= self.right_edge_start:
			return 1

		# if right side is continous 1
		print(self.name, self.right_edge_end, self.left_edge_end)
		if not self.right_edge_end and x >= self.left_edge_end:
			return 1

		# if on the left of characteristic
		if self.left_edge_end and x <= self.left_left_edge_start:
			return 0

		# if on the right of the characteristic
		if self.right_edge_end and x >= self.right_edge_end:
			return 0

		# if in the middle of the characteristic
		if x >= self.left_edge_end and x <= self.right_edge_start:
			return 1

		# if on the left slope
		if self.left_edge_end and x >= self.left_edge_start and x <= self.left_edge_end:
			return self.left_edge_slope[0]*x + self.left_edge_slope[1]

		# if on the right slope
		if self.right_edge_end and x >= self.right_edge_start and x <= self.right_edge_end:
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

			# if function is equal to 1 from (-inf)
			if self.left_edge_end is not None:

				# fit a 1-degree polynomial to two points
				a, b = np.polyfit(x=[self.left_edge_start, self.left_edge_end],
								  y=[0, 1],
								  deg=1)
				return (a, b)

			else:
				return (0, 1)	# there's a horizontal line on left at 1

		# right slope
		if side == 'right':

			# if function is equal to 1 to (inf)
			if self.right_edge_end is not None:

				# fit a 1-degree polynomial to two points
				a, b = np.polyfit(x=[self.right_edge_start, self.right_edge_end],
								  y=[1, 0],
								  deg=1)
				return (a, b)

			else:
				return (0, 0)	# there's a horizontal line on right at 0


class FuzzyAxis:

	def __init__(self, characteristics: List[Characteristic]):
		self.characteristics = characteristics


	def GetCharacteristicsValues(self, x, theta, dx, dtheta):
		for characteristic in self.characteristics:
			print(characteristic.GetValue(x))


def test(x, theta, dx, dtheta):
	BoxOnLeft = Characteristic(name='BoxOnLeft',
							   left_edge_start=-1*float("inf"),
							   right_edge_start=-10,
							   right_edge_end=0)

	BoxOnRight = Characteristic(name='BoxOnRight',
							    left_edge_start=0,
						     	left_edge_end=10,
								right_edge_start=float("inf"))

	BoxPositionAxis = FuzzyAxis(characteristics=[BoxOnLeft, BoxOnRight])

	PendulumTiltedLeft = Characteristic(name="PendulumTiltedLeft",
										left_edge_start=0,
										left_edge_end=0.2,
										right_edge_start=float("inf"))

	PendulumTiltedRight = Characteristic(name="PendulumTiltedRight",
										 left_edge_start=-1*float("inf"),
										 right_edge_start=-0.2,
										 right_edge_end=0)

	PendulumAngleAxis = FuzzyAxis(characteristics=[PendulumTiltedRight, PendulumTiltedLeft])

	PendulumAngleAxis.GetCharacteristicsValues(x, theta, dx, dtheta)


if __name__ == '__main__':
	pass

