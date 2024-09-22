import numpy as np
# from numba import jit, prange, types # jit precompiles functions, prange enables true parallel processing over iterated ranges
# from numba.typed import Dict
import matplotlib.pyplot as plt



# Returns an error value for given geometry
    # Inputs: Steering geometry values and num_fit_points (the length of the output vectors)
    # Outputs: A vector of inner wheel angles, a vector of outer wheel angles, a vector of ideal outer wheel angles
# @jit(nopython=True, parallel=True)
def sim(params):
    ## Unpack params
    # Unpack required variables
    try:
        rack_spacing = params['rack_spacing']
        wt = params['wt']
        l_tierod = params['l_tierod']
        l_str_arm = params['l_str_arm']
        wb = params['wb']
        x_travel = params['x_travel']

    except:
            # print('NOT ALL REQUIRED PARAMATERS WERE PASSED')
            return np.nan
    
    # Unpack optional variables
    phi_lower_bound = params.get('phi_lower_pound', np.radians(15))
    wheel_angle_target = params.get('wheel_angle_target', np.radians(20))
    num_fit_points = params.get('num_fit_points', 100)

    # Determine Phi
    phi = tierod_angle(rack_spacing, wt, l_tierod, l_str_arm, 0)
    
    # Determine rack vectors for inside and outside wheels
    x_i = np.linspace(0, -x_travel, num_fit_points)
    x_o = np.linspace(0, x_travel, num_fit_points)

    # Determine corresponding theta 2 lists
    tierod_angle_i = tierod_angle(rack_spacing, wt, l_tierod, l_str_arm, x_i)
    tierod_angle_o = tierod_angle(rack_spacing, wt, l_tierod, l_str_arm, x_o)
    
    # Determine corresponding theta_i and theta_o
    theta_i = np.pi - wheel_angle(tierod_angle_i, phi)
    theta_o = wheel_angle(tierod_angle_o, phi)
    
    ## Check if results should be discarded
    # If phi too small
    if phi < phi_lower_bound:
        # print('phi bound')
        # return np.nan, np.nan # np.full((3, num_fit_points), np.nan)
        return np.nan

    # If possible turning angle is too small
    # print(f'theta_i: {theta_i}')
    # print(f'theta_oL {theta_o}')
    if max(max(theta_i), max(theta_o)) < wheel_angle_target:
        # print('wheel_angle_bound')
        # return np.nan, np.nan
        return np.nan
        

    # Calculate
    theta_o_ideal = theta_o_ideal_eq(wb, wt, theta_i)
    RMSE = np.linalg.norm(theta_o - theta_o_ideal) / num_fit_points

    # Return Data for Analysis
    # return {'RMSE':RMSE,'params': params, 'theta_i': theta_i, 'theta_o': theta_o, 'theta_o_ideal': theta_o_ideal}
    # print(f'returning: {RMSE}')
    return RMSE



## Helper Functions---------------------------------------------------------------------------------

# Add wheel offset to steering arm angle
# @jit(nopython=True, parallel=True)
def wheel_angle(tierod_angle, phi):
    return tierod_angle + np.pi/2 - phi

# Helper function to calculate ideal outer wheel angle
# @jit(nopython=True, parallel=True)
def theta_o_ideal_eq(wb, wt, theta_i):
    return np.pi/2 - np.arctan((wb) / (wb/np.tan(np.pi/2 - theta_i) + 2*wt))


# Angle of the tierod
# @jit(nopython=True) # Jit has not found a way to parallelize this
def tierod_angle(a, wt, l1, l2, x):
    d = np.sqrt(a**2 + (wt-x)**2)
    theta11 = np.arctan(a/(wt-x))
    theta12 = np.arccos((d**2 + l1**2 - l2**2) / (2*d*l1))
    theta22 = np.arccos((l1**2 + l2**2 - d**2) / (2*l1*l2))
    return theta11 - theta12 + np.pi -theta22