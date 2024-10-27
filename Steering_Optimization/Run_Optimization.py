from Optimize_steering import *
import numpy as np
import time 
import sys



# read cli arguments, clean input
improper_input_reason = ''
if len(sys.argv) != 2:
    improper_input_reason = 'Incorrect number of arguments, input must have 1 argument(resolution of search in mm), setting resolution to 10mm'
else:
    try:
        float(sys.argv[1])
    except:
        improper_input_reason = f'{sys.argv[1]} is not a float, setting resolution to 10mm'

if improper_input_reason:
    print(improper_input_reason)
    step_size = 10
else:
    step_size = float(sys.argv[1]) # [MWh]


# Simulation parameters
num_steps = 500 # Define the number of steps
num_fit_points = 100 # Define granularity
num_graphs = 100 # Number of next best fits to plot
num_retain = 5 # The number of correct cases to maintain


# Constants
wb = 2000 # Wheelbase [mm]
x_travel = 80 # Steering rack travel per direction [mm]
w_track = 800 # Track width [mm]
l_rack = 300 # Steering rack length [mm]


# Geometry Ranges
rack_spacings = np.arange(50, 450 + step_size, step_size)
ls_tierod = np.arange(50, 350 + step_size, step_size)
ls_str_arm = np.arange(50.1, 800 + step_size, step_size) # needs to be larger than ls_str_arm min to avoid divide by 0 error

# Package Inputs
opt_inputs = {
    'w_track': w_track,
    'l_rack': l_rack,
    'wb': wb,
    'x_travel': x_travel,

    'rack_spacings': rack_spacings,
    'ls_tierod': ls_tierod,
    'ls_str_arm': ls_str_arm,

    'num_fit_points': num_fit_points,
    'num_retain': num_retain
}


# opt_inputs = to_typed_dict(opt_inputs)
print('Parameters instantiated...')
sys.stdout.flush()

t1 = time.time()
results_numba = OptimizeSteering(opt_inputs)

print('RESULTS:')
for result in results_numba:
    print(result)



# # WIP
# # Convert out of numba
# results = {}
# for key, value in results_numba.items():
#     results[key] = value

# t2 = time.time()
# print(f'exec time: {t2-t1}')


# print(f'\n\nMin RMSEs: ')
# for i in results:
#     print(f'\t{i["RMSE"]}')


# # Send results to CSV
# import csv

# # Example list of dictionaries
# # data = [
# #     {'name': 'Alice', 'age': 30, 'city': 'New York'},
# #     {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
# #     {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
# # ]

# # Specify the CSV file name
# csv_file = 'Optimizaiton_results.txt'

# # Writing to the CSV file
# with open(csv_file, mode='w', newline='') as file:
#     writer = csv.DictWriter(file, fieldnames=results[0].keys())
#     writer.writeheader()  # Write the header
#     # for result in results:
#     writer.writerows(results)  # Write the data

# print(f'Data written to {csv_file}')








    # num_graphs = params.get('num_graphs', num_retain)

    # if num_graphs > num_retain:
    #     ValueError('num_graphs must be less than num_retain')
    #     return np.nan