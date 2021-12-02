import rozmywanie, defuzyfikacja
from typing import List, Tuple

def get_rules_outputs(x, theta, dx, dtheta) -> Tuple[float]:

	# retrieve all regulation axes
	axes = {axis.name: axis for axis in rozmywanie.initialize_axes()}
	PendulumAngleAxis = axes['PendulumAngleAxis']
	PendulumRotationAxis = axes['PendulumRotationAxis']
	CartPositionAxis = axes['CartPositionAxis']

	# retrieve current readings 
	pendulum_tilt = PendulumAngleAxis.GetCharacteristicsValues(theta)
	pendulum_rotation = PendulumRotationAxis.GetCharacteristicsValues(dtheta)
	cart_position = CartPositionAxis.GetCharacteristicsValues(x)

	# -------------------------RULE 1-------------------------
	# if pendulum on left and rotating left then push cart left
	pendulum_tilted_left = pendulum_tilt['PendulumTiltedLeft']
	pendulum_rotating_left = pendulum_rotation['PendulumRotatingLeft']
	pendulum_angle_push_left = fuzzy_and([pendulum_tilted_left, pendulum_rotating_left])
	
	# -------------------------RULE 2-------------------------
	# if pendulum on right and rotating right then push cart right
	pendulum_tilted_right = pendulum_tilt['PendulumTiltedRight']
	pendulum_rotating_right = pendulum_rotation['PendulumRotatingRight']
	pendulum_angle_push_right = fuzzy_and([pendulum_tilted_right, pendulum_rotating_right])

	# -------------------------RULE 3-------------------------
	# if cart on left of 0 and pendulum in the middle push cart right
	pendulum_centered = pendulum_tilt['PendulumCentered']
	cart_on_left = cart_position['CartOnLeft']
	cart_position_push_right = fuzzy_and([pendulum_centered, cart_on_left])

	# -------------------------RULE 4-------------------------
	# if cart on right of 0 and pendulum in the middle and it's not rotating push cart left
	cart_on_right = cart_position['CartOnRight']
	pendulum_not_rotating = fuzzy_not(fuzzy_and([pendulum_rotating_right, pendulum_rotating_left]))
	cart_position_push_left = fuzzy_and([pendulum_centered, cart_on_right, pendulum_not_rotating])

	print(f'cart_on_left: {cart_on_left}    cart_on_right: {cart_on_right}')
	# compose final outputs
	push_cart_left = fuzzy_or([pendulum_angle_push_left, cart_position_push_left])
	push_cart_right = fuzzy_or([pendulum_angle_push_right, cart_position_push_right])

	return push_cart_left, push_cart_right


def fuzzy_and(values: List[float]) -> float:
	return min(values)


def fuzzy_or(values: List[float]) -> float:
	return max(values)


def fuzzy_not(value: float) -> float:
	return 1.0 - value
