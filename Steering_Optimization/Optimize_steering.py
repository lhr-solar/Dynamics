    # -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 20:03:07 2023

Authors: Jacob Yan, Tristan Houy, Edward Kim
"""
# from numba import dict as nb_dict
from numba import types, typed
import numpy as np
from Simulate_steering import sim
import logging
import warnings
logging.basicConfig(level=logging.WARNING)
warnings.filterwarnings("ignore", category=RuntimeWarning)



# Run optimization
def OptimizeSteering(params):

    

    # Unpack required paramaters
    try:
        # Required params
        w_track = params['w_track']
        l_rack = params['l_rack']
        wb = params['wb']
        x_travel = params['x_travel']

        rack_spacings = params['rack_spacings']
        ls_tierod = params['ls_tierod']
        ls_str_arm = params['ls_str_arm']

    except:
            print('NOT ALL REQUIRED PARAMATERS WERE PASSED')
            return results
    
    wt = (w_track - l_rack)/2 # Equivalent steering thickness [length units passed in]
    
    # Unpack optional variables
    phi_lower_bound = params.get('phi_lower_bound', np.radians(15))
    wheel_angle_target = params.get('wheel_angle_target', np.radians(20))
    num_fit_points = params.get('num_fit_points', 100)
    num_retain = params.get('num_retain', 1)

    # Create initial results
    results = [{'RMSE': np.inf}]*num_retain

    # Prange has essentially no performance improvement over regular iteration
    for i in rack_spacings:
        for j in ls_tierod:
            for k in ls_str_arm:
                params_loop = typed.Dict.empty(types.unicode_type, types.float64)
                # params_loop = {}
                # Static
                params_loop['wt'] = wt
                params_loop['wb'] = wb
                params_loop['x_travel'] = x_travel
                params_loop['num_fit_points'] = num_fit_points
                params_loop['wheel_angle_target'] = wheel_angle_target
                params_loop['pi_lower_bound'] = phi_lower_bound
                # Changing
                params_loop['rack_spacing'] = i
                params_loop['l_tierod'] = j
                params_loop['l_str_arm'] = k
                # Calculate error
                RMSE = sim(params_loop)
                params_loop['RMSE'] = RMSE
                
                # Add to list if not nan, smaller than largest value
                if not np.isnan(RMSE) and RMSE < results[-1]['RMSE']:
                    results = results[0:-1]
                    results.append(params_loop)
                    results.sort(key=lambda x: x['RMSE'])
                    # print(f'new min: {RMSE}')

    return results
                    


# Convert normal python dictionaries to typed dicts (needed for numba)
def to_typed_dict(dict):
    typed_dict = typed.Dict.empty(types.unicode_type, types.ListType(types.float64))
    
    for key, value in dict.items():
        
        typed_list = typed.List.empty_list(types.float64) # Make typed list

        # Check if list
        if isinstance(value, list) or isinstance(value, np.ndarray): 
            typed_list.extend(value) # Extend good for lists
        else:
            typed_list.append(float(value)) # append, cast for single values

        typed_dict[key] = typed_list  # Match key to typed dict

    return typed_dict

