import numpy as np

# Create a NumPy array of floats
array_of_floats = np.array([1.0, 2.5, 3.7, 4.2, 5.9])

# Extract the first and last items using pattern matching
def matching(array_of_floats):
    match array_of_floats:
        case [first, *_, last]:
            print("First item:", first)
            print("Last item:", last)
        case _: print("non")

if __name__ == "__main__":
    matching(array_of_floats)
