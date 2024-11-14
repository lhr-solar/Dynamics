from Optimize_steering import *
import numpy as np
import time 
import sys
import csv


# read cli arguments, clean input
improper_input_reason = ''
if len(sys.argv) < 2:
    improper_input_reason = 'Incorrect number of arguments, input arguments are:\n\tresolution: The resolution of the search in mm, defaulting to 10mm\n\toutput filename: Optional Paramater. If passed, outputs the results in a CSV with the given filename'
else:
    try:
        float(sys.argv[1])
    except:
        improper_input_reason = f'{sys.argv[1]} is not a float, setting resolution to 10mm'

# Assign defaults for improperly formatted run
if improper_input_reason:
    print(improper_input_reason)
    step_size = 10
else:
    step_size = float(sys.argv[1]) # [MWh]

# See if output csv requested
try:
    filename = sys.argv[2]
except:
    filename = ''

## Define constants
# Simulation parameters
num_fit_points = 100 # Define granularity
num_retain = 10 # The number of correct cases to maintain

# Geometry constants
wb = 2500 # Wheelbase [mm]
x_travel = 82.55 # Steering rack travel per direction [mm]
w_track = 1500 # Track width [mm]
l_rack = 386.715 # Steering rack length [mm]
phi_upper_bound = np.radians(0) # positive phi is towards the outboard side

# Geometry variable ranges
rack_spacings = np.arange(50, 700 + step_size, step_size)
ls_tierod = np.arange(50, 700 + step_size, step_size)
ls_str_arm = np.arange(50.1, 700 + step_size, step_size) # needs to be larger than ls_str_arm min to avoid divide by 0 error


# Package Inputs
opt_inputs = {
    'w_track': w_track,
    'l_rack': l_rack,
    'wb': wb,
    'x_travel': x_travel,
    'phi_upper_bound': phi_upper_bound,

    'rack_spacings': rack_spacings,
    'ls_tierod': ls_tierod,
    'ls_str_arm': ls_str_arm,

    'num_fit_points': num_fit_points,
    'num_retain': num_retain,
}


# Run optimization and timekeep
print('Precompiling')
sys.stdout.flush()
t1 = time.time()
results_numba = OptimizeSteering(opt_inputs)
t2 = time.time()
print(f'Elapsed searching time: {t2-t1}s')
print('RESULTS:')
for result in results_numba:
    print(result)


# If a filename was passed in, create csv
if filename: 
    # Convert typed dict to python dicts
    results = [dict(value) for value in results_numba]

    # Write file
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f'Data written to {filename}')
