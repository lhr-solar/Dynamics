import math

class Wet_Pavement():
    def __init__(self, M, Iw, nW, dW, Im, nG, V, deacc,delay_time,peak_brake ):
        self.M = M  # M - mass of the car
        self.Iw = Iw  # Iw - tire moment of inertia
        self.nW = nW  # nW - number of wheels
        self.dW = dW  # dW - wheel diameter
        self.Im = Im  # Im - motor moment of inertia
        self.nG = nG  # nG - gear ratio of the transmission
        self.V = V  # V - initial velocity of the solar car
        self.dac = deacc  # Deacc - minimum deceleration of the car (which is 4.72 m/s^2)
        self.dt = delay_time # Delay time between the brakes applied and signal to stop
        self.bp = peak_brake # Peak Brake - peak braking coefficient for a wetted pavement (0.59 from the Solar Car Primer)
    def effective_mass(self):
        return self.M + ((4 * self.nW * self.Iw) / (math.pow(self.dW, 2))) \
               + ((4 * math.pow(self.nG, 2) * self.Im) / (math.pow(self.dW, 2)))

    def kinetic_energy(self):
        return 0.5 * math.pow(self.V, 2) * self.effective_mass()

    def braking_torque(self):
        return (0.278 * self.effective_mass() * self.dac * (self.dW/2))\
               /(1 - ((self.dt * self.dac)/self.V))

    def braking_force(self):
        return self.braking_torque()/(self.dW/2)

    def acceptability(self):
        if self.braking_force() < (self.bp * self.M * 9.81):
            return False
        else:
            return True

        # True means acceptable || False means unacceptable
        # We are comparing the results of the braking force of the solar car vs the required braking force for wet pavement
