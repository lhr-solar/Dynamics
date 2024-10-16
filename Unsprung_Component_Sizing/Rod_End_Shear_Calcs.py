## DEFINE INPUTS

import math

# Define Geometry
pi = math.pi #3.1415926535897932384626433
l1 = 150.87 #[mm] vertical distance from lower rod end to tire contact patch
l2 = 452.56 #[mm] vertical distance from upper rod end to tire contact patch
l3 = 115.83 #[mm] vertical distance from lower rod end to axle
l4 = 185.86 #[mm] vertical distance from upper rod end to axle
l5 = 34.80 #[mm] lower rod end unsupported length
l6 = 14.01 #[mm] upper rod end unsupported length
w = 75.28 #[mm] lateral distance from rod ends to tire contact patch
rw = 10.5 * 25.4 #[in -> mm] wheel radius
r1 = (.625 / 2) * 25.4 #[in -> mm] radius of 5/8" rod end
r2 = (.3125 / 2) * 25.4 #[in-mm] radius of 1/4" rod end

# Define Loads
car_mass = 700 * 4.45 #[lbf -> N]
FB = car_mass / 4 * 5 #[N] gg load /4 wheels for conservative car weight of 700lbs
Fs = car_mass / 4 #[N] 1g load /4 wheels for conservative car weight of 700lbs
Fb = car_mass / 4 #[N] 1g load /4 wheels for conservative car weight of 700lbs
Tb = Fb * rw #[Nmm] applied torque from braking

# Define Material Properties
yield_strength = 460 #[MPa]
shear_yield = yield_strength / 2 #[MPa]


## SOLVE
# Solve for reaction forces
F1x = (FB*w + Fs*l2) / (l1-l2)
F2x = -F1x - Fs
F1y = -FB
F1z = (Fb*l4 - Tb) / (l3 + l4)
F2z = Fb - F1z

# Calculate Areas and moments of inertia
A1 = pi * r1**2 #[mm^2] cross sectional area of the bottom rod end
A2 = pi * r2**2 #[mm^2] cross sectional area of the top rod end
I1 = pi/4 * r1**4 #[mm^4] 2nd moment of area of the bottom rod end
I2 = pi/4 * r2**4 #[mm^4] 2nd moment of area of the top rod end

# Solve for bottom rod end stresses
sigma1x = (abs(F1x)/A1) + (abs(F1y)*l5) * r1 / I1 #[MPa]
sigma1y = 0 #[GPa]
tau1 = 4/3 * abs(F1z) / A1 #[GPa]

# Solve for top rod end stresses
sigma2x = abs(F2x)/A2 + (abs(F2z)*l6) * r2 / I2 #[MPa]
sigma2y = 0 #[GPa]
tau2 = 0 #[GPa]


# Solving for brake disc boost
r1 = 1.5 #[mm]
l7 =  1 #[mm]
A1 = pi * r1**2 #[mm^2] cross sectional area of the bottom rod end
I1 = pi/4 * r1**4 #[mm^4] 2nd moment of area of the bottom rod end
FC = Tb/(254/2) #[N] force applied at bolts in motor

sigma1x = (abs(FC)*l7) * r1 / I1
sigma1y = 0
tau1 = 4/3* FC/A1


sigma2x = 0
sigma2y = 0
tau2 = 0.1

# Calculate max shear
tau1_MAX = ((sigma1x - sigma1y)**2 + (2*tau1)**2)**0.5 / 2 #[GPa]
tau2_MAX = ((sigma2x - sigma2y)**2 + (2*tau2)**2)**0.5 / 2 #[GPa]

# Calculate safety factor
SF_tresca1 = shear_yield / tau1_MAX
SF_tresca2 = shear_yield / tau2_MAX


## DISPLAY OUTPUT
print('---------FORCES---------')
print(f'F1x: {F1x} N')
print(f'F2x: {F2x} N')
print(f'F1y: {F1y} N')
print(f'F1z: {F1z} N')
print(f'F2z: {F2z} N')

print('---------STRESSES---------')
print(f'sigma1x: {sigma1x} GPa')
print(f'sigma1y: {sigma1y} GPa')
print(f'sigma2x: {sigma2x} GPa')
print(f'sigma1y: {sigma1y} GPa')
print(f'tau1: {tau1} GPa')
print(f'tau2: {tau2} GPa')

print('---------MAX SHEAR---------')
print(f'tau1 MAX: {tau1_MAX} GPa')
print(f'tau2 MAX: {tau2_MAX} GPa')

print('---------SAFETY FACTORS---------')
print(f'SF_tresca1: {SF_tresca1}')
print(f'SF_tresca2: {SF_tresca2}')

print('---------------')
