import math

class Wet_Pavement():
    def __init__(self, M, Iw, nW, dW, Im, nG, V, deacc,delay_time,peak_brake,x1,x2,y,dp,rd,dm):
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
        self.x1 = x1 # x1 = horizontal distance between front wheels and CG (center of gravity) in terms of meters
        self.x2 = x2 # x2 = horizontal distance between front wheels and CG (center of gravity) in terms of meters
        self.y = y # y = vertical distance between ground and CG in terms of meters
        self.dp = dp # dp = the diameter of the pistons
        self.rd = rd # rd = radius to the center of where the brake pads in the calipers contact the rotor
        self.dm = dm # dm = the diameter of the master cylinder
    def effective_mass(self):
        return self.M + ((4 * self.nW * self.Iw) / (math.pow(self.dW, 2))) \
               + ((4 * math.pow(self.nG, 2) * self.Im) / (math.pow(self.dW, 2)))

    def kinetic_energy(self):
        return 0.5 * math.pow(self.V, 2) * self.effective_mass()

    def weight_transfer(self):
    # weight of car is 600 pounds
    # 60% front || 40% back
        front = self.effective_mass() * 9.81 * 0.6
        back = self.effective_mass() * 9.81 * 0.4
    # Weight Transfer for front and back (returns a tuple)
        inertial_force = self.effective_mass() * self.dac
        back_force = ((self.x1 * self.effective_mass()*9.81)-(inertial_force * self.y)) / (self.x1 + self.x2)
        front_force = ((self.x2 * self.effective_mass()*9.81)+(inertial_force * self.y)) / (self.x1 + self.x2)
        return (front_force,back_force)

    def braking_torque(self):
        return (0.278 *  self.weight_transfer()[0] * self.dac * (self.dW))\
               /(1 - ((self.dt * self.dac)/self.V))

    def braking_force(self):
        return self.braking_torque()/(self.dW)

    def acceptability(self):
        if self.braking_force() < (self.bp * self.M * 9.81):
            return False
        else:
            return True

    # True means acceptable || False means unacceptable
    # We are comparing the results of the braking force of the solar car vs the required braking force for wet pavement

    def pad_friction(self):
        pad_friction_force = self.braking_torque()/(2*self.rd)
        return pad_friction_force

    def piston_pressure(self):
        return (self.pad_friction()/0.2)/(math.pi * 0.25 * math.pow(self.dp, 2))

    def pedal_force(self):
        return self.piston_pressure() * 0.25 * math.pi * math.pow(self.dm,2)


