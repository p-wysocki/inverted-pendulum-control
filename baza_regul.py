import rozmywanie, defuzyfikacja
from typing import List, Tuple

def get_rules_outputs(x, theta, dx, dtheta) -> Tuple[float]:

	# retrieve all regulation axes
	axes = {axis.name: axis for axis in rozmywanie.initialize_axes()}
	PendulumAngleAxis = axes['PendulumAngleAxis']
	PendulumRotationAxis = axes['PendulumRotationAxis']

	# retrieve current readings 
	pendulum_tilt = PendulumAngleAxis.GetCharacteristicsValues(theta)
	pendulum_rotation = PendulumRotationAxis.GetCharacteristicsValues(dtheta)

	# -------------------------RULE 1-------------------------
	# if pendulum on left and rotating left then push cart left
	pendulum_tilted_left = pendulum_tilt['PendulumTiltedLeft']
	pendulum_rotating_left = pendulum_rotation['PendulumRotatingLeft']
	push_cart_left = fuzzy_and([pendulum_tilted_left, pendulum_rotating_left])
	
	# -------------------------RULE 2-------------------------
	# if pendulum on right and rotating right then push cart right
	pendulum_tilted_right = pendulum_tilt['PendulumTiltedRight']
	pendulum_rotating_right = pendulum_rotation['PendulumRotatingRight']
	push_cart_right = fuzzy_and([pendulum_tilted_right, pendulum_rotating_right])

	return push_cart_left, push_cart_right


def fuzzy_and(values: List[float]) -> float:
	return min(values)


def fuzzy_or(values: List[float]) -> float:
	return max(values)


def fuzzy_not(value: float) -> float:
	return 1.0 - value
