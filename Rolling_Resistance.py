import math
import pandas as pd
import matplotlib.pyplot as plt

# Equations from the Solar Car Primer || Will be using this formula for now (returns the FORCE of rolling resistance)
def tire_contribution(K,d0,dw,p,p0,N):
    h = 0.5 * (d0/dw) * math.pow((p/p0),0.3072) * \
        (dw - math.pow(math.pow(dw,2)- (4*N/math.pi) * ((2.456+0.251*dw)/(19.58+0.5975*p)),0.5))
    return h * K

# Equation from the OneDrive RR Resource Page
'''def coefficient_friction(K,dw,p,p0,w,w0):
    crr = K * (w0 / w) * math.pow((p / p0), 0.3072) * \
        (dw - math.pow(math.pow(dw, 2) - (4 * w / math.pi) * ((2.456 + 0.251 * dw) / (19.58 + 5975 * p)), 0.5))
    return crr

def K(F,dw,p0,w,w0):
    K = (F/w0)/(dw - math.pow(math.pow(dw, 2) - (4 * w / math.pi) * ((2.456 + 0.251 * dw) / (19.58 + 5975 * p0)), 0.5))
    return K
'''

def main():
    # p0 = pressure of the tire at which the rolling resistance experiment was conducted
    # p = max safe pressure || whatever pressure we assign

    # d0 = actual diameter of the wheel
    # dw = diameter of wheel w/o tire influence
    # weight of car is 600 pounds
    # 60% front || 40% back

    # Results of Rolling Resistance: Graph of Power Consumption at Different Velocities, Different Air Pressure
    # Constants && Assumptions used for the Following Calculations:
    # d0 = 21.67 in (actual diameter)
    # dw = 16 in (advertised nominal diameter)
    # Total Weight of car will be 600 lbs: 60% front || 40% back
    # p0 = 80 psi
    # p = 75 psi
    # K = 2.47 (derived from experimental data)

    # ALL values must be in SI units


    # Front Wheel
    # velocity values from 0 mph to 30 mph || will convert to meters per second when calculating power consumption
    c1 = tire_contribution(2.47, 16*0.0254, 21.67*0.0254, 75*6894.76, 80*6894.76, 600 * 0.6 * 0.5*0.453592)
    #c2 = coefficient_friction(2.47,21.67,30,25,600 * 0.6 * 0.5,0)
    power_consumption = []
    speed = []
    for i in range(31):
        # Using the First Formula
        power_consumption.append((i * 0.44704) * c1)
        speed.append(i*0.44704)
    # Plot the power consumption vs speed
    d = {'Speed (mph)':speed,'Power Consumption':power_consumption}
    df = pd.DataFrame(d)
    plt.scatter(speed,power_consumption)
    plt.xlabel('Speed (m/s)')
    plt.ylabel('Power Consumption (W) ')
    plt.title('Power Consumption of Front Wheels')
    plt.show()
    power_consumption = []
    speed = []
    c1b = tire_contribution(2.47, 16*0.0254, 21.67*0.0254, 75*6894.76, 80*6894.76, 600 * 0.4 * 0.5*0.453592)
    # Back Wheel
    for i in range(31):
        # Using the First Formula
        power_consumption.append((i * 0.44704) * c1b)
        speed.append(i * 0.44704)
    # Plot the power consumption vs speed
    db = {'Speed (mph)': speed, 'Power Consumption': power_consumption}
    dfb = pd.DataFrame(db)
    plt.scatter(speed, power_consumption)
    plt.xlabel('Speed (m/s)')
    plt.ylabel('Power Consumption (W) ')
    plt.title('Power Consumption of Back Wheels')
    plt.show()


main()

# Air Drag of Wheel and Bearing Friction (considered negligible)

'''def air_drag_solid_rims(ns,ds,r2,r1,rw,rho,V):
    cd = 1.2
    coeff_r = (1/8)*((ns*ds)*(math.pow(r2,4)-math.pow(r1,4))*rho*cd*V)/(math.pow(rw,2))
    return (coeff_r*V)/(rw)

def air_drag_spoked_rims(rho,rw,V,visc):
    Rey_W = (V*rw)/visc
    if Rey_W > 3*math.pow(10,5):
        cm = 0.146 / (math.pow(Rey_W, 1 / 5))
    else:
        cm = 3.87 / (math.pow(Rey_W, 1 / 2))
    return 0.5 * math.pow(rw, 3) * rho * V * cm'''

'''def bearing_friction(a0,a1,V,rw,L,L1):
    c = 30/(math.pi*rw)
    torque = (a0 + a1*c*V)*math.pow((L/L1),2)
    return torque 
'''