

def get_cart_force(push_cart_left, push_cart_right) -> float:
	"""
	Defuzzyfies the output force of the cart.

	Arguments:
		fuzzy values of force characteristics.
	Returns:
		force
	"""
	max_push_left_force = -550.0
	max_push_right_force = 550.0

	# check if they are non-zero
	if push_cart_left or push_cart_right:
		force = (push_cart_left*max_push_left_force + push_cart_right*max_push_right_force)/(push_cart_left + push_cart_right)
		return force

	# else return 0 to avoid division by zero
	return 0
