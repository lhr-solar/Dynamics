    # -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 20:03:07 2023

Authors: Jacob Yan, Tristan Houy, Edward Kim
"""
def OptimizeSteering():
    # from numba import jit, prange
    # from numba.typed import Dict
    import numpy as np
    import matplotlib.pyplot as plt
    from Simulate_steering import sim
    import heapq
    from alive_progress import alive_bar
    import logging

    logging.basicConfig(level=logging.WARNING)
    '''-------------------------------------------------OPTIMIZATION PARAMETERS---------------------------------------------------------'''
    # Simulation parameters
    num_steps = 50 # Define the number of steps
    num_fit_points = 10000 # Define granularity

    # Constants
    phi_lower_bound = np.radians(-15) # Lower bound for phi in radians [Deg] -> [Rad]
    wb = 2000 # Wheelbase [mm]
    x_travel = 80 # Steering rack travel [mm]
    w_track = 800 # Track width [mm]
    l_rack = 300 # Steering rack length [mm]

    # Dependent Variables
    wt = (w_track - l_rack)/2 # Equivalent steering thickness [mm]

    # Variables
    rack_spacing_lower =  50 # Front/back distance between steering rack axis and control arm bearing mounting [mm]
    rack_spacing_upper =  450

    l_tierod_lower = 50 # Tierod length [mm]
    l_tierod_upper = 350

    l_str_arm_lower = 50.1 # Distance from control arm mounts to steering arm mount [mm]
    l_str_arm_upper = 800

    # Plotting parameters
    num_graphs = 100 # Number of next best fits to plot

    base_dict = {
        'wt': wt,
        'wb': wb,
        'x_travel': x_travel,
        'num_fit_points': num_fit_points,
        'phi_lower_bound': phi_lower_bound
    }
    print('Parameters instantiated...')
    """
    ----------------------------------------------------------------------------------------------------------------------------------------
    Everything above this point is a variable you can change.
    Everything below is code you do not change.
    """

    # Define initial variable vectors
    rack_spacing=np.linspace(rack_spacing_lower, rack_spacing_upper, num_steps)
    l_tierod=np.linspace(l_tierod_lower, l_tierod_upper, num_steps)
    l_str_arm=np.linspace(l_str_arm_lower, l_str_arm_upper, num_steps)

    # Define helper function to pull parameters
    # @jit(nopython=True,parallel=False) 
    def Sweep_inputs(rack_spacing_range, l_tierod_range, l_str_arm_range):
        results = {}
        params = {}
        params.update(base_dict)
        # for i in prange(rack_spacing_range.size):
        #     for j in prange(l_tierod_range.size):
        #         for k in prange(l_str_arm_range.size):
        with alive_bar(rack_spacing_range.size * l_tierod_range.size * l_str_arm_range.size) as bar:
            for i in range(rack_spacing_range.size):
                for j in range(l_tierod_range.size):
                    for k in range(l_str_arm_range.size):
                        params.update({'rack_spacing': rack_spacing_range[i], 
                                    'l_tierod': l_tierod_range[j], 
                                    'l_str_arm': l_str_arm_range[k]
                                    })
                        
                        # sim_output = sim(params)
                        RMSE = sim(params)
                        
                    
                        # if sim != np.nan:
                        if not np.isnan(RMSE):
                            # results[sim_output['RMSE']] = params
                            results[RMSE] = params
                        bar()
        return results




    # Running the simulation
    print('Running sim...')
    simulation_results = Sweep_inputs(rack_spacing, l_tierod, l_str_arm)

    # Find Optimal set
    best_RMSE = heapq.nsmallest(num_graphs, simulation_results.keys())

    # Retrieve the optimal values



    # optimal_rack_spacing = simulation_results[best_RMSE]['rack_spacing']
    # optimal_l_tierod = simulation_results[best_RMSE]['l_tierod']
    # optimal_l_str_arm = simulation_results[best_RMSE]['l_str_arm']

    # Output Ideal value information
    print("Minimum RMSE:", best_RMSE[0])
    # print("Optimal Geometry:")
    # print("Rack Spacing:", optimal_rack_spacing)
    # print("Tierod Length:", optimal_l_tierod)
    # print("Steering Arm Length:", optimal_l_str_arm)



















    # Plotting setup
    # plt.figure()
    # # Save plotting range
    # x_range = [min(theta_i_plot)-0.05, max(theta_i_plot)+0.05]
    # y_range = [min(theta_o_ideal_plot)-0.05, max(theta_o_ideal_plot)+0.05]
    # y_ticks = []
    # for i in list(np.linspace(y_range[0], y_range[1], 5)):
    #     y_ticks.append(round(i, 3))


    # # Plot ideal solution and best optimized solution
    # plt.plot(theta_i_plot, theta_o_ideal_plot, 'k-', linewidth = 8, label = 'Ideal Curve')
    # plt.plot(theta_i_plot, theta_o_plot, 'r--', linewidth = 2, label = f'Best Fit Curve: rsme = {min_rmse}')

    # # Calculate and plot curves for the next 100 best fitting curves 

    # for i in sorted_rmse[1:num_graphs+1]:

    #     min_rmse_filtered_index = rmse_results.index(i)

    #     # Map this index back to the original index in simulation_results
    #     min_rmse_original_index = valid_indices[min_rmse_filtered_index]

    #     # Calculate the index in each dimension using the original index
    #     index_rack_spacing = (min_rmse_original_index // (num_steps ** 2)) % num_steps
    #     index_l_tierod = (min_rmse_original_index // num_steps) % num_steps
    #     index_l_str_arm = min_rmse_original_index % num_steps

    #     # Retrieve the optimal values
    #     optimal_rack_spacing = rack_spacing[index_rack_spacing]
    #     optimal_l_tierod = l_tierod[index_l_tierod]
    #     optimal_l_str_arm = l_str_arm[index_l_str_arm]

    #     # Cacluate performance from geometry
    #     [theta_i_plot, theta_o_plot, theta_o_ideal_plot] = sim(optimal_rack_spacing, wt, optimal_l_tierod, optimal_l_str_arm, wb, x_travel, num_fit_points, phi_lower_bound)
    #     plt.plot(theta_i_plot, theta_o_plot, '--', 'color', 'tab:gray', linewidth = 0.25)

    # # Format and display figure
    # plt.title(f'Comparison of inner and outer wheel curves with step count of {num_steps}')
    # plt.xlabel('Inner Wheel Angle [rad]')
    # plt.ylabel('Outer Wheel Angle [rad]')
    # plt.xlim(x_range)
    # plt.ylim(y_range)
    # plt.legend(loc='best')
    # plt.yticks(y_ticks, y_ticks) 
    # plt.show()




if __name__ == '__main__':
    OptimizeSteering()