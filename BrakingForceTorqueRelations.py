# This script takes a torque input and determines the various forces and ratios needed for the braking system
# This program is not intended to give specific values
# V 1.0


# Variables (PLACEHOLDERS)
# ALL MUST BE IN SI UNITS (meters, kgNewtons, newtons)

# Determined:
pedal_mechanical_advantage = 1.80841602268  # Calculated with this program
hydraulic_advantage = 21.2064
# Surface area of master cylinder = 1.88^2 * pi in^2, slave cylinder SA= pi in^2, ratio =1.88^2, feeds into 6 slave
# pistons(3 caliper assem. 2 pistons each), =(1.88/1)^2 * 6, see trade study parts

# Measured:
brake_rotor_radius = 0.1016 # see trade study parts
coef_friction = 0.275  # See trade study, brake pad paper should verify with our equipment
real_pedal_force = 400  # See trade study pedal force paper
brake_torque = 428.59952784  # see DecelerationCalculations.py in gitub
number_of_brakes = 3
piston_stroke = 0.02794  # See trade study parts


# Calculations start here


def calculated_pedal_force():
    return brake_torque / brake_rotor_radius / hydraulic_advantage / pedal_mechanical_advantage / coef_friction


# equals the product of the needed mechanical and hydraulic advantages
def calculated_total_advantage():
    return brake_torque / brake_rotor_radius / real_pedal_force / coef_friction


def calculated_brake_torque():
    return real_pedal_force * pedal_mechanical_advantage * hydraulic_advantage * brake_rotor_radius * coef_friction


def pedal_displacement():
    return piston_stroke * pedal_mechanical_advantage

# Display


print("CALCULATED AND GIVEN PARAMETERS MUST MATCH\nAdjust mechanical and hydraulic advantages to correspond with the "
      "calculated total advantage\n")
print("Given parameters:")
print("Pedal force: ", real_pedal_force, "N")
print("Total advantage: ", str(pedal_mechanical_advantage * hydraulic_advantage))
print("Brake torque : ", brake_torque, " Nm")


print("\nCalculated values(should match given parameters): ")
print("Pedal force needed: ", calculated_pedal_force(), "N")
print("Total advantage needed: ", calculated_total_advantage())
print("Brake torque needed: ", calculated_brake_torque(), " Nm")


print("\nMin pedal displacement: ", pedal_displacement(), " M")
