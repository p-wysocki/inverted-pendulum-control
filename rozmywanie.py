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
		self.left_edge_start = left_edge_start
		self.right_edge_start = right_edge_start
		
		# optional arguments
		self.left_edge_end = left_edge_end
		self.right_edge_end = right_edge_end

		# calculate 1st degree polynomials
		self.left_edge_slope = self.get_slope(side='left')
		self.right_edge_slope = self.get_slope(side='right')


	def get_slope(self, side: str) -> tuple[float]:
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

	def __init__(self, classes: List[Characteristic]):
		pass


if __name__ == '__main__':
	pendulum_on_left = Characteristic('pendulum_on_left', 500, 1000, 750, 1200)
