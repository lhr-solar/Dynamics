# Evaluate which method of calculating tierod angles is faster

print('test')
import numpy as np
import time
from alive_progress import alive_bar
t0 = time.time()

from numba import jit, prange

t1 = time.time()


# Implementation utilizing rotation of reference frame
@jit(nopython=True, parallel=False) # Jit has not found a way to parallelize this
def tierod_angle_rf(a, wt, l1, l2, x):

    # Define initial variables
    d = np.sqrt(a**2 + (wt-x)**2)
    theta11 = np.arctan(a/(wt-x))
    theta12 = np.arccos((d**2 + l1**2 - l2**2) / (2*d*l1))
    theta1 = theta11 - theta12

    # Calculate tierod angle
    tierod_angle = np.arctan((a - l1*np.sin(theta1)) / (wt - x - l1*np.cos(theta1)))
    return tierod_angle
    

# Implementation utilizing a static frame
@jit(nopython=True, parallel=False) # Jit has not found a way to parallelize this
def tierod_angle_ff(a, wt, l1, l2, x):

    # Define initial variables
    d = np.sqrt(a**2 + (wt-x)**2)
    theta11 = np.arctan(a/(wt-x))
    theta12 = np.arccos((d**2 + l1**2 - l2**2) / (2*d*l1))
    theta22 = np.arccos((l1**2 + l2**2 - d**2) / (2*l1*l2))
    return theta11 - theta12 + np.pi -theta22


# Implementation utilizing a static frame, law of sines
@jit(nopython=True, parallel=False) # Jit has not found a way to parallelize this
def tierod_angle_ff_sin(a, wt, l1, l2, x):

    # Define initial variables
    d = np.sqrt(a**2 + (wt-x)**2)
    theta11 = np.arctan(a/(wt-x))
    theta12 = np.arccos((d**2 + l1**2 - l2**2) / (2*d*l1))
    theta22 = np.arcsin(d/l2*np.sin(theta12))
    return theta11 - theta12 + theta22


# Run with normal loop
loops = 10**7

a = 200
wt = 250
l1 = 200
l2 = 150
x = 0

# Test 1: ff with no sin is much faster (less trig operations?) but overall difference is in the order of 5%
with alive_bar(loops) as bar:
    for i in range(loops): 
        temp = tierod_angle_rf(a, wt, l1, l2, x)
        bar()

# with alive_bar(loops) as bar:
#     for i in range(loops): 
#         temp = tierod_angle_ff(a, wt, l1, l2, x)
#         bar()

# with alive_bar(loops) as bar:
#     for i in range(loops): 
#         temp = tierod_angle_ff_sin(a, wt, l1, l2, x)
#         bar()


# prange is faster on the order of 5%
# with alive_bar(loops) as bar:
#     for i in range(loops): 
#         temp = tierod_angle_ff(a, wt, l1, l2, x)
#         bar()

# with alive_bar(loops) as bar:
#     for i in prange(loops): 
#         temp = tierod_angle_ff(a, wt, l1, l2, x)
#         bar()
