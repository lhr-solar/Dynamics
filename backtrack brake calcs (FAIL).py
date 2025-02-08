import numpy as np

print("New Entry -------------------------------")

# =============================================================================
# 1. PARAMETERS & UNIT CONVERSIONS
# =============================================================================

# --- Driver Input ---
brake_pedal_force = 400  # N (driver pedal force)

# --- Hydraulic System (Master Cylinder) ---
# Dimensions given in mm; convert to meters for SI consistency.
master_cylinder_diameter_mm = 15.875  # mm
master_cylinder_stroke_mm = 27.94  # mm
num_master_cylinders = 2

# Convert to meters:
master_cylinder_diameter = master_cylinder_diameter_mm / 1000  # m
master_cylinder_stroke = master_cylinder_stroke_mm / 1000  # m

# Use correct area formula: A = π*(d/2)^2 per cylinder.
total_master_cylinder_area = (
    np.pi * (master_cylinder_diameter / 2) ** 2 * num_master_cylinders
)  # m²

# --- Hydraulic System (Caliper) ---
# The provided caliper piston area is for one piston in mm².
caliper_piston_area_mm2 = 793.5468  # mm² per piston
num_pistons_per_caliper = 2
# Update: There are 2 calipers per front wheel, and 2 front wheels, so total calipers = 4.
num_calipers_total = 4

# Convert mm² to m² (1 mm² = 1e-6 m²):
caliper_piston_area = caliper_piston_area_mm2 * 1e-6  # m² per piston

# Total caliper piston area (all calipers):
total_caliper_area = (
    caliper_piston_area * num_pistons_per_caliper * num_calipers_total
)  # m²

# --- Advantages ---
# Hydraulic Advantage (HA) is the ratio of total caliper piston area to total master cylinder area.
HA = total_caliper_area / total_master_cylinder_area

# --- Brake Geometry ---
# Rotor and Wheel dimensions (given in mm; convert to m)
rotor_diameter_mm = 171.45  # mm
wheel_diameter_mm = 484.886  # mm
rotor_diameter = rotor_diameter_mm / 1000  # m
wheel_diameter = wheel_diameter_mm / 1000  # m
wheel_radius = wheel_diameter / 2  # m
rotor_radius = rotor_diameter / 2  # m

# --- Vehicle Parameters ---
car_mass = 269.18370632627  # kg
g = 9.81  # m/s²

# Center of gravity height and wheelbase (given in mm; convert to m)
cg_height = 0.33419288  # m
wheelbase = 2.25  # m

# --- Friction Coefficients ---
# Tire friction coefficients: 0.4 for wet and 0.8 for dry.
mu_tire_wet = 0.5
mu_tire_dry = 0.8

# Brake pad (pad-to-rotor) friction coefficient (typical values are in the 0.3-0.4 range):
mu_pad = 0.4

weight_front_percent = 0.7
weigh_rear_percent = 0.3

# --- Weight Distribution (Assumed) ---
# Assume 60% of the static weight is on the front.
static_front_weight = weight_front_percent * car_mass * g  # N
static_rear_weight = weigh_rear_percent * car_mass * g  # N

# =============================================================================
# 2. DECELERATION & DYNAMIC LOAD CALCULATIONS
# =============================================================================
# The following functions compute the dynamic normal force per front wheel
# including weight transfer due to braking. The load transfer is:
#   load_transfer = m * a * (cg_height / wheelbase)
# and the dynamic normal force on both front wheels is:
#   N_front_total = static_front_weight + load_transfer
# with N_front_per_wheel = N_front_total / 2.


def compute_deceleration(mu_tire):
    # A simple equilibrium based on:
    #   m * a = μ * (static_front_weight + m * a * (cg_height/wheelbase))
    # Solving for a gives:
    #   a = (μ * (static_front_weight/m)) / (1 - μ*(cg_height/wheelbase))
    a = (mu_tire * weight_front_percent * g) / (1 - mu_tire * (cg_height / wheelbase))
    return a


def compute_dynamic_normal_force(a):
    # Compute load transfer due to braking deceleration a.
    load_transfer = car_mass * a * (cg_height / wheelbase)  # N
    N_front_total = static_front_weight + load_transfer  # N (for both front wheels)
    N_front_per_wheel = N_front_total / 2  # N per front wheel
    return N_front_per_wheel, load_transfer


# For our two cases, we compute the deceleration available (which, under our friction model,
# is the limit when tires are at the friction threshold).
a_wet = compute_deceleration(mu_tire_wet)
a_dry = compute_deceleration(mu_tire_dry)

print("=== Deceleration Limits (Tire Friction) ===")
print(f"Wet conditions (μ_tire = {mu_tire_wet}): deceleration = {a_wet:.2f} m/s²")
print(f"Dry conditions (μ_tire = {mu_tire_dry}): deceleration = {a_dry:.2f} m/s²")

# Compute dynamic normal force per front wheel:
N_front_wet, load_transfer_wet = compute_dynamic_normal_force(a_wet)
N_front_dry, load_transfer_dry = compute_dynamic_normal_force(a_dry)

# =============================================================================
# 3. FORCE CHAIN: FROM TIRE TO ROTOR
# =============================================================================
# For each front wheel:
# 1. Maximum braking force at the tire contact patch is:
#       F_tire = μ_tire * N_front_per_wheel.
# 2. The corresponding wheel braking torque is:
#       T_wheel = F_tire * wheel_radius.
# 3. To generate T_wheel, the brake pads must apply a total force:
#       F_pad_total = T_wheel / (rotor_radius * μ_pad).
# (This force is generated by the calipers pressing the brake pads against the rotor.)

# Wet conditions:
F_tire_wet = mu_tire_wet * N_front_wet  # N per front wheel
T_wheel_wet = F_tire_wet * wheel_radius  # Nm per front wheel
F_pad_total_wet = T_wheel_wet / (
    rotor_radius * mu_pad
)  # N required per front wheel (total force on both pads)
# For both front wheels:
F_pad_total_front_wet = 2 * F_pad_total_wet

# Dry conditions:
F_tire_dry = mu_tire_dry * N_front_dry
T_wheel_dry = F_tire_dry * wheel_radius
F_pad_total_dry = T_wheel_dry / (rotor_radius * mu_pad)
F_pad_total_front_dry = 2 * F_pad_total_dry

print("\n=== Brake Forces at the Rotor (Per Front Wheel) ===")
print("Wet conditions:")
print(f"  Dynamic normal force per front wheel: {N_front_wet:.2f} N")
print(f"  Maximum tire braking force per front wheel: {F_tire_wet:.2f} N")
print(f"  Wheel braking torque per front wheel: {T_wheel_wet:.2f} Nm")
print(
    f"  Required pad force per front wheel (total for both pads): {F_pad_total_wet:.2f} N"
)
print("Dry conditions:")
print(f"  Dynamic normal force per front wheel: {N_front_dry:.2f} N")
print(f"  Maximum tire braking force per front wheel: {F_tire_dry:.2f} N")
print(f"  Wheel braking torque per front wheel: {T_wheel_dry:.2f} Nm")
print(
    f"  Required pad force per front wheel (total for both pads): {F_pad_total_dry:.2f} N"
)

# =============================================================================
# 4. SOLVE FOR REQUIRED PEDAL RATIO
# =============================================================================
# The hydraulic system provides a force multiplication (Hydraulic Advantage, HA) defined as:
#       HA = (Total Caliper Area) / (Total Master Cylinder Area)
#
# The force available at the calipers from the driver's pedal force is:
#       F_caliper_total = (Pedal Ratio) * F_pedal * HA
#
# For the system to deliver the needed force at the rotor, we require:
#       F_caliper_total = Total required pad force for front wheels.
#
# Thus, the required pedal ratio (MA_pedal) is:
#       MA_pedal = (Total required pad force for front wheels) / (F_pedal * HA)
#
# We'll compute this for both wet and dry conditions.

MA_pedal_required_wet = F_pad_total_front_wet / (brake_pedal_force * HA)
MA_pedal_required_dry = F_pad_total_front_dry / (brake_pedal_force * HA)

print("\n=== Required Pedal Ratio (Mechanical Advantage) ===")
print(f"Wet conditions: Required pedal ratio = {MA_pedal_required_wet:.2f}")
print(f"Dry conditions: Required pedal ratio = {MA_pedal_required_dry:.2f}")

# =============================================================================
# 5. COMMENTS
# =============================================================================
"""
Explanation:
-----------
- For each condition, we first compute the dynamic normal force (including weight transfer)
  on each front wheel.
- The tire friction force F_tire = μ_tire * N_front gives the maximum braking force
  available at the contact patch.
- This force, multiplied by the wheel radius, provides the wheel braking torque.
- To achieve that torque, the brake pads must apply a force given by:
      F_pad_total = T_wheel / (rotor_radius * μ_pad)
- Since there are two front wheels, we multiply by 2 to get the total pad force required.
- The hydraulic system multiplies the master cylinder force by HA, and the pedal mechanism
  multiplies the driver’s pedal force by the pedal ratio.
- Setting:
      (Pedal Ratio) * F_pedal * HA = Total required pad force (front)
  and solving for the pedal ratio gives the value computed above.
  
This pedal ratio tells you by how much the driver’s pedal force must be amplified (in addition
to the hydraulic multiplication) to provide the necessary caliper force that will produce the required
braking torque at the rotor. This value is critical for designing the pedal mechanism and will serve
as an input for further structural simulations on the rotor.
  
"""

# End of code.
