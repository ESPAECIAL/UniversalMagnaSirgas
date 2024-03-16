import numpy as np


# Extract the first and last items using pattern matching
def matching(array_of_floats):
    match array_of_floats:
        case [float(first), *_, float(last)]:
            print("First item:", first)
            print("Last item:", last)
        case _:
            print("non")


if __name__ == "__main__":
    # Create a NumPy array of floats
    array_of_floats = np.array([1.0, 2.5, 3.7, 4.2, 5.9])
    matching(array_of_floats)
    array_of_floats = np.array([1, 2.5, 3.7, 4.2, 5])
    matching(array_of_floats)
