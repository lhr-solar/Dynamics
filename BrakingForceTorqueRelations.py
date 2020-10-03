# This script takes a torque input and determines the various forces and ratios needed for the braking system
# This program is not intended to give specific values
# V 1.0


# Variables (PLACEHOLDERS)
# ALL MUST BE IN SI UNITS (meters, kgNewtons, newtons)

# Determined:
pedal_mechanical_advantage = 5
hydraulic_advantage = 40

# Measured:
brake_rotor_radius = 1
coef_friction = 0.8
real_pedal_force = 10
brake_torque = 1000
number_of_brakes = 2
max_pedal_displacement = 0.5


# Calculations start here


def calculated_pedal_force():
    return number_of_brakes * brake_torque / brake_rotor_radius / hydraulic_advantage / pedal_mechanical_advantage


# equals the product of the needed mechanical and hydraulic advantages
def calculated_total_advantage():
    return brake_torque * number_of_brakes / brake_rotor_radius / real_pedal_force


def calculated_brake_torque():
    return real_pedal_force * pedal_mechanical_advantage * hydraulic_advantage * brake_rotor_radius / number_of_brakes


def max_caliper_displacement():
    return max_pedal_displacement / pedal_mechanical_advantage / hydraulic_advantage


# Display
print("CALCULATED AND GIVEN PARAMETERS MUST MATCH\nAdjust mechanical and hydraulic advantages to correspond with the "
      "calculated total advantage\n")
print("Given parameters:")
print("Pedal force: ", real_pedal_force, "N")
print("Total advantage: ", str(pedal_mechanical_advantage * hydraulic_advantage))
print("Brake torque: ", brake_torque, " Nm")


print("\nCalculated values: ")
print("Pedal force: ", calculated_pedal_force(), "N")
print("Total advantage: ", calculated_total_advantage())
print("Brake torque: ", calculated_brake_torque(), " Nm")


print("\nMax caliper displacement: ", max_caliper_displacement(), " M")
