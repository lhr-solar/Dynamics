# Drag Coefficient is determined through simulations of the body || body team is responsible for providing the Drag coefficient value

# Use SI units for each input variable


def drag_force(Cd,rho,V,A):
    return 0.5 * Cd * rho * (V ** 2) * A

def drag_power(Cd,rho,V,A):
    return drag_force(Cd, rho, V, A) * V

def lift_force(Cl,rho,V,A):
    return 0.5 * Cl * rho * (V ** 2) * A



# try and minimize the lift force as much as possible (near zero)


# Cd - drag coefficient
# Rho - density of the air
# V - velocity of the solar car
# A - frontal area of the solar car

# Values for Cd and A will be determined using simulations for each different solar car body
