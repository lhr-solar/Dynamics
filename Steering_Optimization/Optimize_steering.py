    # -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 20:03:07 2023

Authors: Jacob Yan, Tristan Houy, Edward Kim
"""
from numba import types, typed
import numpy as np
from Simulate_steering import sim
import logging
import warnings
import sys
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
    
    
    # Unpack optional variables
    phi_upper_bound = params.get('phi_upper_bound', np.radians(30))
    wheel_angle_target = params.get('wheel_angle_target', np.radians(20))
    num_fit_points = params.get('num_fit_points', 100)
    num_retain = params.get('num_retain', 1)

    # Create initial results list
    results = [{'MSE': np.inf}]*num_retain

    # Define static values per loop
    params_loop_base = typed.Dict.empty(types.unicode_type, types.float64)
    params_loop_base['w_track'] = w_track
    params_loop_base['l_rack'] = l_rack
    params_loop_base['wb'] = wb
    params_loop_base['x_travel'] = x_travel
    params_loop_base['num_fit_points'] = num_fit_points
    params_loop_base['wheel_angle_target'] = wheel_angle_target
    params_loop_base['phi_upper_bound'] = phi_upper_bound


    # Prange has essentially no performance improvement over regular iteration
    # Iterate through combinations
    print('Starting Search')
    sys.stdout.flush()
    for i in rack_spacings:
        for j in ls_tierod:
            for k in ls_str_arm:
                              
                # Changing values per loop
                params_loop = params_loop_base.copy()
                params_loop['rack_spacing'] = i
                params_loop['l_tierod'] = j
                params_loop['l_str_arm'] = k
                # Calculate error
                MSE = sim(params_loop)
                params_loop['MSE'] = MSE
                
                # Add to list if not nan, smaller than largest value
                if not np.isnan(MSE) and MSE < results[-1]['MSE']:
                    params_loop['l_rack'] = l_rack
                    results = results[0:-1]
                    results.append(params_loop)
                    results.sort(key=lambda x: x['MSE'])

    return results
                    
