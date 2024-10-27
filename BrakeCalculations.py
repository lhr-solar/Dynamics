import numpy as np

brake_pedal_force = 70 * 4.448 # lbf

### Hydraulic
## Master Cylinder
# from wilwood's website https://www.wilwood.com/MasterCylinders/MasterCylinderList?group=Compact%20Remote%20Master%20Cylinder
master_cylinder_diameter_options = [5/8, 3/4, 13/16, 7/8, 15/16, 1, 9/8] #[in]
master_cylinder_diameter = master_cylinder_diameter_options[5] * 25.4 #[in->mm]
master_cylinder_stroke = 1.12 * 25.4 #[in -> mm]
num_master_cylinders = 2
total_master_cylinder_area = np.pi * master_cylinder_diameter**2 * num_master_cylinders
print("Total Master Cylinder Area: ", total_master_cylinder_area, "mm^2")

## Caliper Cylinders
caliper_cylinder_diameter = 34 #[mm]
pistons_per_caliper = 2 
num_calipers = 4
num_caliper_pistons = num_calipers * pistons_per_caliper
total_caliper_piston_area = np.pi * caliper_cylinder_diameter**2 * num_caliper_pistons
print("Total Caliper Cylinder Area: ", total_caliper_piston_area, "mm^2")


HA = total_caliper_piston_area / total_master_cylinder_area
print("Hydraulic Advantage: ", HA)

## Mechanical Advantage
MA = 3
Advantage = HA * MA

## Torque
# Front Brake Disc
disc_diameter = 11.5 * 25.4 #[in->mm]
# Motor Brake Disc
#disc_diameter = 310 #[mm] brake disc

wheel_diameter = 21 * 25.4 #[in-mm]

torque_advantage = disc_diameter / wheel_diameter
print("Torque Advantage", torque_advantage)

car_mass = 730 / 2.205 #[lbm -> kg]
target_deceleration = 5 #[m/s^2], regs limit is 4.72 m/s^2

coef_friction_disc = 0.5

total_force = brake_pedal_force * Advantage * coef_friction_disc * torque_advantage
deceleration = total_force / car_mass

caliper_cylinder_stroke = master_cylinder_stroke / HA
print("Total Force: ", total_force, "N")
print("Piston Travel: ", caliper_cylinder_stroke, "mm")
print("Deceleration: ", deceleration, "m/s")
print("Target Deceleration: ", target_deceleration, "m/s")
