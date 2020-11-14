# This script determines the maximum deceleration possible for the car given different models and determines the
# proportion of that ideal deceleration needed to meet standards
# This script is not intended to give specific values
# V 1.2


# variables (PLACEHOLDERS ONLY)
# ALL VARIABLES SHOULD BE IN SI UNITS (meters and kilograms)
tire_spacing = 2.452  # from body
center_of_mass_distance_from_front = 0.9808 # estimated from TWSC model
car_mass = 317.515  # (liberal estimate) goal weight of 550 lbs plus 150lbs for driver
wheel_radius = 0.2752  # from parts
num_front_wheels = 2
coef_friction = 0.8  # Estimated for dry pavement
# constants
g = 9.81


def torque_general(weight_proportion):
    return coef_friction * g * wheel_radius * car_mass * weight_proportion


# Approximations begin here
#
# balanced is calculated using the weight distribution of the car at rest
# twsc_model is calculated using the winning solar car estimate of 70% weight on the front wheel
#   (front suspension and brakes section)
# upper bound for the front wheel assumes that 100% of the car's weight is concentrated on the front wheel
# upper bound for the back is the same as the balanced equation
#
# deceleration is given for the car as a whole
# torque is given for each wheel


def torque_balanced_front():
    weight_distribution = (tire_spacing - center_of_mass_distance_from_front) / tire_spacing
    return torque_general(weight_distribution) / num_front_wheels


def torque_twsc_model_front():
    return torque_general(0.7) / num_front_wheels


def torque_upper_bound_front():
    return torque_general(1) / num_front_wheels


def deceleration_amount(torque):
    return torque * num_front_wheels / (car_mass * wheel_radius)


def standards_torque():
    return 0.5 * g * car_mass * wheel_radius / num_front_wheels


def meet_standards(torque):
    return deceleration_amount(standards_torque()) > deceleration_amount(torque)


# proportion of ideal torque without slipping needed to pass regulation
def prop_ideal_torque(torque):
    return standards_torque() / torque


# Display


# max torque for tire
# print("Balanced:\n\tFront: ", str(torque_balanced_front()))
# print("\ntwsc:\n\tFront: ", str(torque_twsc_model_front()))
# print("\nUpper Bound:\n\tFront: ", str(torque_upper_bound_front()))
# print("\nMeets Standards:", str(meet_standards()))


print("Torque required to meet standards(whole car): ", str(standards_torque() * num_front_wheels))

print("\nBalanced model deceleration: ", str(deceleration_amount(torque_balanced_front() * num_front_wheels)))
print("Proportion of ideal torque needed: ", prop_ideal_torque(torque_balanced_front()))

print("\nTwsc model deceleration: ", str(deceleration_amount(torque_twsc_model_front() * num_front_wheels)))
print("Proportion of ideal torque needed: ", prop_ideal_torque(torque_twsc_model_front()))

print("\nUpper bound model deceleration: ", str(deceleration_amount(torque_upper_bound_front() * num_front_wheels)))
print("Proportion of ideal torque needed: ", prop_ideal_torque(torque_upper_bound_front()))
