import numba
from numba import types
from numba.typed import Dict
from numba import njit

print(numba.__version__)

# Step 1: Define the inner typed dictionary type
InnerDictType = Dict.empty(key_type=types.unicode_type, value_type=types.float64)

# Step 2: Define the outer typed dictionary type
OuterDictType = Dict.empty(key_type=types.unicode_type, value_type=InnerDictType)

# Step 3: Function to create and populate the outer typed dictionary
@njit
def create_outer_dict():
    outer_dict = OuterDictType()

    # Create and populate the first inner dictionary
    inner_dict1 = InnerDictType()
    inner_dict1["a"] = 1.1
    inner_dict1["b"] = 2.2

    # Add the first inner dictionary to the outer dictionary
    outer_dict["dict1"] = inner_dict1

    # Create and populate the second inner dictionary
    inner_dict2 = InnerDictType()
    inner_dict2["c"] = 3.3
    inner_dict2["d"] = 4.4

    # Add the second inner dictionary to the outer dictionary
    outer_dict["dict2"] = inner_dict2

    return outer_dict

# Step 4: Usage
outer_dict_instance = create_outer_dict()

# Print the outer dictionary and its contents
for key in outer_dict_instance.keys():
    print(f"{key}: {outer_dict_instance[key]}")
