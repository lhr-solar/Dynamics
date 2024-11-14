import sys
import os
import csv
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as shape
from Simulate_steering import real_geometry_performance, theta_o_ideal_eq

def draw_steering(params, x_rack, subplot):
    # Unpack params
    try:
        rack_spacing = float(params['rack_spacing'])
        w_track = float(params['w_track'])
        l_rack = float(params['l_rack'])
        l_tierod = float(params['l_tierod'])
        l_str_arm = float(params['l_str_arm'])
    except:
        print('Specified tile does not have the required variables for draw_steering')
        exit()
    wte = (w_track - l_rack)/2 # Equivalent steering thickness/effective track width [length units passed in]
    
    # Define points for the steering geometry
    rack_end_i = np.array([-l_rack/2 + x_rack, 0])
    rack_end_o = np.array([l_rack/2 + x_rack, 0])
    upright_pivot_i = np.array([-w_track/2, rack_spacing])
    upright_pivot_o = np.array([w_track/2, rack_spacing])
    theta_i, theta_o, phi = real_geometry_performance(rack_spacing, wte, l_tierod, l_str_arm, -x_rack, x_rack)
    str_arm_end_i = upright_pivot_i - l_str_arm*np.array([np.cos(theta_i - phi), np.sin(theta_i - phi)])
    str_arm_end_o = upright_pivot_o - l_str_arm*np.array([np.cos(theta_o + phi), np.sin(theta_o + phi)])

    # Define wheel rectangle
    wheel_dims = np.array([80, 533.4]) # [mm] asthetic for wheel
    wheel_i = shape.Rectangle((upright_pivot_i-wheel_dims/2), wheel_dims[0], wheel_dims[1], angle=np.rad2deg(theta_i)-90, rotation_point='center', alpha=.75 )
    wheel_o = shape.Rectangle((upright_pivot_o-wheel_dims/2), wheel_dims[0], wheel_dims[1], angle=np.rad2deg(theta_o)-90, rotation_point='center', alpha=.75)

    # Define lines for plotting
    tierods = np.array([rack_end_i, str_arm_end_i, rack_end_o, str_arm_end_o]).transpose()
    tierods_x = tierods[0].reshape(2,2).transpose()
    tierods_y = tierods[1].reshape(2,2).transpose()
    str_arms = np.array([str_arm_end_i, upright_pivot_i, str_arm_end_o, upright_pivot_o]).transpose()
    str_arms_x = str_arms[0].reshape(2,2).transpose()
    str_arms_y = str_arms[1].reshape(2,2).transpose()
    rack = np.array([rack_end_i, rack_end_o]).transpose()
 


    ## Plot
    subplot.set_title(f'Geometry: x_rack = {x_rack}')
    # Draw marker points
    subplot.scatter(x_rack, 0, marker='*', c='k')
    subplot.scatter(upright_pivot_i[0], upright_pivot_i[1], marker='.', c='k')
    subplot.scatter(upright_pivot_o[0], upright_pivot_o[1], marker='.', c='k')    

    # Draw linkages, centerline and wheels
    subplot.plot([0,0], [upright_pivot_i[1], 0], '--k')
    subplot.plot(tierods_x, tierods_y, c='k')
    subplot.plot(str_arms_x, str_arms_y, c='b')
    subplot.plot(rack[0], rack[1], c='r')
    subplot.add_patch(wheel_i)
    subplot.add_patch(wheel_o)

    # Set aspect ratio equal
    subplot.set_aspect('equal', adjustable='box')


# Draws a graph at max steering angle, and one where the rack is centered
def draw_all_steering(params, fig):
    x_travel = float(params['x_travel'])
    max_angle_ax = fig.add_subplot(1,2,1)
    zero_angle_ax = fig.add_subplot(1,2,2)
    draw_steering(params, 0, zero_angle_ax)
    draw_steering(params, x_travel, max_angle_ax)


def graph_wheel_angles(params, fig):
    # Unpack params
    try:
        
        rack_spacing = float(params['rack_spacing'])
        w_track = float(params['w_track'])
        wb = float(params['wb'])
        l_rack = float(params['l_rack'])
        l_tierod = float(params['l_tierod'])
        l_str_arm = float(params['l_str_arm'])
        x_travel = float(params['x_travel'])
    except:
        print('Specified tile does not have the required variables for graph_wheel_angles')
        exit()

    wte = (w_track - l_rack)/2 # Equivalent steering thickness/effective track width [length units passed in]
    num_plot_points = 100
    x_i = np.linspace(0, -x_travel, num_plot_points)
    x_o = np.linspace(0, x_travel, num_plot_points)

    theta_i, theta_o, phi = real_geometry_performance(rack_spacing, wte, l_tierod, l_str_arm, x_i,x_o, verbose=False)
    theta_o_ideal = theta_o_ideal_eq(wb, wte, theta_i, )
    
    # Plot    
    ax_line = fig.add_subplot(2,1,1)
    ax_scatter = fig.add_subplot(2,1,2)
    ax_line
    ax_line.plot(np.rad2deg(theta_i)-90, np.rad2deg(theta_o)-90, 'b', label='Real')
    ax_line.plot(np.rad2deg(theta_i)-90, np.rad2deg(theta_o_ideal)-90, 'k', label = 'Ideal')
    ax_scatter.scatter(np.rad2deg(theta_i)-90, np.rad2deg(theta_o)-90, c='b', marker='x', label='Real')
    ax_scatter.scatter(np.rad2deg(theta_i)-90, np.rad2deg(theta_o_ideal)-90, c='k',marker='+', label='Ideal')

    ax_line.set_xlabel('theta_i')
    ax_line.set_ylabel('theta_o')
    ax_scatter.set_xlabel('theta_i')
    ax_scatter.set_ylabel('theta_o')

    ax_line.legend()
    ax_scatter.legend()

    ax_line.grid()
    ax_scatter.grid()




# read cli arguments, clean input
improper_input_reason = ''
if len(sys.argv) < 2:
    improper_input_reason = 'Incorrect number of arguments, must include a filename to read from'
else:
    if not os.path.isfile(sys.argv[1]):
        improper_input_reason = f'{sys.argv[1]} has not been found at:\n{os.getcwd()}\\{sys.argv[1]}'
if improper_input_reason:
    print(improper_input_reason)
    exit()
filename = sys.argv[1]
print(f'successful filename of {filename}')

# Read CSV
with open(filename, 'r') as file:
    Data = list(csv.reader(file))
# Find title indexes
indexes = {}
for var in Data[0]:
    indexes[var] = list(Data[0]).index(var)


# Perform operations on desired rows (i+1 rows)
num_best_plot = 1
for i in range(num_best_plot):
    print(f'\n#{i+1} best geometry:')
    # Fill vals dictionary with geometry from the selected row
    params = {}
    for var in indexes.keys():
        params[var] = Data[i+1][indexes[var]]
    print(f'var: {params}')

    # Define drawing figures
    fig_wheel_angles = plt.figure(1, layout='tight')
    fig_draw_geom = plt.figure(2, layout='tight')
    # Draw graphs
    graph_wheel_angles(params, fig_wheel_angles)
    draw_all_steering(params, fig_draw_geom)

    # Outputs
    sys.stdout.flush()
    plt.show()
