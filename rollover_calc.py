# Parameters for the Vehicle
# All units are in SI (m,N)

tire_radius = float(input('Enter tire radius: '))
vehicle_track_width = float(input('Enter vehicle track width: '))
vehicle_wheelbase = float(input('Enter vehicle wheelbase: '))
weight_distribution_front = float(
    input('Enter weight distribution for front axle: '))
weight_distribution_rear = float(
    input('Enter weight distribution for rear axle: '))
vehicle_mass = float(input('Vehicle mass in kg: '))
cg_height = float(input('Vertical location for center of gravity: '))
vehicle_weight = vehicle_mass*9.81

# Lateral Load Calcs

Ay = 1  # [g]
wl = ((vehicle_weight * vehicle_track_width * 0.5) +
      (vehicle_weight * Ay * cg_height))/vehicle_track_width
delta_w = wl - (vehicle_weight*0.5)
print('Assuming the vehicle is turning right!')
print("Weight SI [N]:", vehicle_weight)
print("Left Side Load [N]:", (vehicle_weight/2) + delta_w)
print("Right Side Load [N]:", (vehicle_weight/2) - delta_w)
if ((vehicle_weight/2) - delta_w) < 0:
    print("Rollover will occur")
else:
    print("No rollover")

# Longitudinal Load Calcs

a = vehicle_wheelbase*(1-weight_distribution_front)  # [m]
b = vehicle_wheelbase*(1-weight_distribution_rear)  # [m]
l = a + b
Ax = 1  # [g]
delta_Wx = (vehicle_weight * Ax * cg_height)/l
print("Total Load Transfer for 1G Braking [N]:", delta_Wx)

# 1G Turning

left_side_normal_force = ((vehicle_weight/2) + delta_w)
right_side_normal_force = ((vehicle_weight/2) - delta_w)
left_side_front_wheel = ((vehicle_weight/2) + delta_w) * \
                         weight_distribution_front
right_side_front_wheel = ((vehicle_weight/2) - delta_w) * \
                          weight_distribution_front
left_side_rear_wheel = ((vehicle_weight/2) + delta_w) - left_side_front_wheel
right_side_rear_wheel = ((vehicle_weight/2) - delta_w) - right_side_front_wheel
if left_side_normal_force >= 0 and right_side_normal_force >= 0:
    print("Front Right Wheel:", right_side_front_wheel)
    print("Front Left Wheel:",left_side_front_wheel)
    print("Rear Right Wheel:",right_side_rear_wheel)
    print("Rear Left Wheel:",left_side_rear_wheel)
else:
    print("Rollover will occur")


# 1G Braking 
front_axle = (vehicle_weight * weight_distribution_front) + delta_Wx
rear_axle = (vehicle_weight * weight_distribution_rear) - delta_Wx
print('Front Axle [N]:',front_axle)
print('Rear Axle [N]:',rear_axle)
print("Front Wheel [N]",front_axle/2)
print("Back Wheel [N]",rear_axle/2)

# 2G Bump 

front_left_wheel_2G = ((vehicle_weight * weight_distribution_front)/2) * 2 
front_right_wheel_2G = ((vehicle_weight * weight_distribution_front)/2) * 2 
rear_left_wheel_2G = ((vehicle_weight * weight_distribution_rear)/2) * 2
rear_right_wheel_2G = ((vehicle_weight * weight_distribution_rear)/2) * 2
print("Front Left Wheel 2G [N]:",front_left_wheel_2G)
print("Front Right Wheel 2G [N]:",front_right_wheel_2G)
print("Rear Left Wheel 2G [N]:",rear_left_wheel_2G)
print("Rear Right Wheel 2G [N]:",rear_right_wheel_2G)

# Worst Case Scenario (1g Brake + 1g Turn + 2g Bump)

L1 = vehicle_weight*weight_distribution_front * 0.5
R1 = vehicle_weight*weight_distribution_front * 0.5
L2 = vehicle_weight*weight_distribution_rear * 0.5
R2 = vehicle_weight*weight_distribution_rear * 0.5

L1 = (L1 + (delta_Wx * 0.5) + (delta_w * 0.5)) * 2
R1 = (R1 + (delta_Wx * 0.5) - (delta_w * 0.5))* 2
L2 = (L2 - (delta_Wx * 0.5) + (delta_w * 0.5))* 2
R2 = (R2 - (delta_Wx * 0.5) - (delta_w * 0.5))* 2
print("Front Left Wheel 2G [N]:",L1)
print("Front Right Wheel 2G [N]:",R1)
print("Rear Left Wheel 2G [N]:",L2)
print("Rear Right Wheel 2G [N]:",R2)
