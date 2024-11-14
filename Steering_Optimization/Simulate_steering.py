import numpy as np
from numba import njit # jit precompiles functions, prange enables true parallel processing over iterated ranges
import sys
# NEED TO DOWNLOAD SCIPY TO RUN PROPERLY

# Returns an error value for given geometry
    # Inputs: Steering geometry values and num_fit_points (the length of the output vectors)
    # Outputs: A vector of inner wheel angles, a vector of outer wheel angles, a vector of ideal outer wheel angles
@njit(parallel=False)
def sim(params):

    # Unpack required variables
    try:
        
        rack_spacing = params['rack_spacing']
        w_track = params['w_track']
        l_rack = params['l_rack']
        l_tierod = params['l_tierod']
        l_str_arm = params['l_str_arm']
        wb = params['wb']
        x_travel = params['x_travel']

        phi_upper_bound = params['phi_upper_bound']
        wheel_angle_target = params['wheel_angle_target']
        num_fit_points = int(params['num_fit_points'])

    except:
            print('NOT ALL REQUIRED PARAMATERS WERE PASSED sim steering')
            return np.nan
    

    # Determine rack vectors for inside and outside wheels
    wte = (w_track - l_rack)/2 # Equivalent steering thickness/effective track width [length units passed in]
    x_i = np.linspace(0, -x_travel, num_fit_points)
    x_o = np.linspace(0, x_travel, num_fit_points)

    # Find phi so that wheels are straight when rack is centered
    phi = str_arm_angle(rack_spacing, wte, l_tierod, l_str_arm, 0) - np.pi/2 # minus pi over 2 to bring it back to the angle wrt the wheel instead of the horizontal reference
    
    # Determine corresponding theta 2 lists
    str_arm_angle_i = str_arm_angle(rack_spacing, wte, l_tierod, l_str_arm, x_i)
    str_arm_angle_o = str_arm_angle(rack_spacing, wte, l_tierod, l_str_arm, x_o)
    
    # Determine corresponding theta_i and theta_o
    theta_i = np.pi - wheel_angle(str_arm_angle_i, phi)
    theta_o = wheel_angle(str_arm_angle_o, phi)
    
    ## Check if results should be discarded
    # Condition 1: Geometry is capable of reaching target turning angle for turning radius
    # Condition 2: Ensure phi is not too far outboard
    # Condition 3: Remove NAN geometries to save calculation time
    max_theta_o = max(theta_o)
    if (max_theta_o < wheel_angle_target + np.pi/2) or (phi > phi_upper_bound) or (np.isnan(max_theta_o)):
        return np.nan
        
    # Calculate difference between ideal and actual performance
    theta_o_ideal = theta_o_ideal_eq(wb, w_track, theta_i)
    MSE = np.linalg.norm(theta_o - theta_o_ideal) / num_fit_points

    return MSE



## Helper Functions---------------------------------------------------------------------------------
# Copy pasted from above implementation because Numba is going to make me tear my hair out and won't
# neatly take this function without making the implementation disgusting. Please update this if any
# changes are made to the above function
def real_geometry_performance(rack_spacing, wte, l_tierod, l_str_arm, x_i, x_o, verbose=False):
    # Determine Phi
    phi = str_arm_angle(rack_spacing, wte, l_tierod, l_str_arm, 0) - np.pi/2 # minus phi over 2 to bring it back to the angle wrt the wheel instead of the horizontal reference
    
    # Determine corresponding theta 2 lists
    str_arm_angle_i = str_arm_angle(rack_spacing, wte, l_tierod, l_str_arm, x_i)
    str_arm_angle_o = str_arm_angle(rack_spacing, wte, l_tierod, l_str_arm, x_o)
    
    # Determine corresponding theta_i and theta_o
    theta_i = np.pi - wheel_angle(str_arm_angle_i, phi)
    theta_o = wheel_angle(str_arm_angle_o, phi)

    # Print log data for debugging if asked to
    if verbose:
        print(f'phi: {np.rad2deg(phi)} deg\nstr_arm_angle_i: {np.rad2deg(str_arm_angle_i)} deg\nstr_arm_angle_o: {np.rad2deg(str_arm_angle_o)} deg\ntheta_i: {np.rad2deg(theta_i)} deg\ntheta_o: {np.rad2deg(theta_o)} deg')

    return theta_i, theta_o, phi

# Add wheel offset to steering arm angle
@njit(parallel=False)
def wheel_angle(str_arm_angle, phi):
    return str_arm_angle - phi

# Helper function to calculate ideal outer wheel angle
@njit(parallel=True)
def theta_o_ideal_eq(wb, w_track, theta_i):
    return np.pi/2 - np.arctan((wb) / (wb/np.tan(np.pi/2 - theta_i) + 2*w_track))


# Angle of the steering arm
@njit(parallel=False)
def str_arm_angle(a, wte, l1, l2, x):
    
    d = np.sqrt(a**2 + (wte-x)**2)#, dtype=np.float64)
    theta11 = np.arctan(a/(wte-x))
    theta12 = np.arccos((d**2 + l1**2 - l2**2) / (2*d*l1))
    theta22 = np.arccos((l1**2 + l2**2 - d**2) / (2*l1*l2))
    return theta11 - theta12 + np.pi -theta22