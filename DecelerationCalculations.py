# equations should be verified before using data
# V 1.1


# variables (PLACEHOLDERS ONLY)
# ALL VARIABLES SHOULD BE IN SI UNITS (meters and kilograms)
tire_spacing = 2
center_of_mass_distance_from_front = 1
car_mass = 181.437
wheel_radius = 1
number_of_front_wheels = 2
number_of_back_wheels = 2
# constants
g = 9.81
coef_friction = 0.8


def balanced_torque_sans_weight(weight):
    return coef_friction * g * wheel_radius * weight


def torque_general(weight_proportion):
    return balanced_torque_sans_weight(car_mass * weight_proportion)


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
    return torque_general(weight_distribution) / number_of_front_wheels


def torque_balanced_back():
    weight_distribution = center_of_mass_distance_from_front / tire_spacing
    return torque_general(weight_distribution) / number_of_back_wheels


def torque_twsc_model_front():
    return torque_general(0.7) / number_of_front_wheels


def torque_twsc_model_back():
    return torque_general(0.3) / number_of_back_wheels


def torque_upper_bound_front():
    return torque_general(1) / number_of_front_wheels


def torque_upper_bound_back():
    weight_distribution = center_of_mass_distance_from_front / tire_spacing
    return torque_general(weight_distribution) / number_of_back_wheels


def deceleration_amount(torque):
    return torque * number_of_front_wheels / (car_mass * wheel_radius)


def standards_torque():
    return 0.5 * g * car_mass * wheel_radius / number_of_front_wheels


def meet_standards(torque):
    return deceleration_amount(standards_torque() * number_of_front_wheels) > deceleration_amount(torque)


# Display


# max torque for tire
# print("Balanced:\n\tFront: ", str(torque_balanced_front()))
# print("\ntwsc:\n\tFront: ", str(torque_twsc_model_front()))
# print("\nUpper Bound:\n\tFront: ", str(torque_upper_bound_front()))
# print("\nMeets Standards:", str(meet_standards()))
print("Balanced model deceleration: ", str(deceleration_amount(torque_balanced_front() * number_of_front_wheels)),
      "\nMeets standards: ",
      str(meet_standards(deceleration_amount(torque_balanced_front() * number_of_front_wheels))))
print("Twsc model deceleration: ", str(deceleration_amount(torque_twsc_model_front() * number_of_front_wheels)),
      "\nMeets standards: ",
      str(meet_standards(deceleration_amount(torque_twsc_model_front() * number_of_front_wheels))))
print("Upper bound model deceleration: ", str(deceleration_amount(torque_upper_bound_front() * number_of_front_wheels)),
      "\nMeets standards: ", str(meet_standards(deceleration_amount(torque_upper_bound_front() *
                                                                    number_of_front_wheels))))
