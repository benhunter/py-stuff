import numpy as np

from pprint import pprint

# numpy arrays
# copy versus view

# rotate
# https://numpy.org/doc/stable/reference/generated/numpy.rot90.html#numpy.rot90
# note that rotations return views, not new arrays

list_a = [[0, 1], [2, 3]]
array_a = np.array(list_a)
print(array_a)
print(np.rot90(array_a))  # rotate counter clockwise
print(np.rot90(array_a, axes=(1, 0)))  # rotate clockwise
print(np.rot90(array_a, k=0))  # rotate counter clockwise 0 times (same as original)

# flip
print("Flip:")
print(np.flip(array_a))
print("Flip axis 0:")
print(np.flip(array_a, axis=0))
print("Flip axis 1:")
print(np.flip(array_a, axis=1))

# All possible flips and rotations with two dimensions
orientations = [np.rot90(array_a, k=k) for k in range(4)]  # rotations
orientations += [
    np.flip(array_a, axis=axis) for axis in [None, 0, 1]
]  # flips
orientations += [
    np.flip(np.rot90(array_a, k=1), axis=axis) for axis in [None, 0, 1]
]  # flip the first rotation

pprint(orientations)

# edges and flipped edges
array_a_faces = [array_a[0], array_a[-1], array_a[:,0], array_a[:,-1]]
array_a_flipped = np.flip(array_a)
array_a_flipped_faces = [array_a_flipped[0], array_a_flipped[-1], array_a_flipped[:,0], array_a_flipped[:,-1]]
print(array_a_faces)
print(array_a_flipped_faces)



# List[str] to nparray
list_str = ["12","34"]
array_s = np.array(list_str)
array_s = np.array([[c for c in s] for s in list_str])
print(array_s)
print(type(array_s))

print(np.fliplr(array_s))


# Type hints with numpy:
# https://numpy.org/devdocs/reference/typing.html

