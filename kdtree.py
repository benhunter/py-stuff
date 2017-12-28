# from https://en.wikipedia.org/wiki/K-d_tree

import pprint
from collections import namedtuple

import geopy.distance


class KDNode(namedtuple('KDNode', 'location left_child right_child key')):
    def __repr__(self):
        return pprint.pformat(tuple(self))


def build_kdtree(point_list, depth=0):
    """
    Credit to implementation at https://en.wikipedia.org/wiki/K-d_tree
    :param point_list: Must be a list of lists, where the each item is a list of coordinates in each axis followed by
        an ID. For example: [[[latitude1, longitude1], id1], [[latitude2, longitude2], id2], ...].
    :param depth: The current depth in the K-D Tree.
    :return: KDNode object including its left and right children.
    """
    try:
        k = len(point_list[0][0])  # assumes all points have the same dimension
    except IndexError as e:
        return None

    # Select axis based on depth so that axis cycles through all valid values
    axis = depth % k

    # Sort point_list and choose median as pivot element
    point_list.sort(key=lambda point: point[0][axis])
    median = len(point_list) // 2  # choose median

    # Create node and construct subtrees
    return KDNode(
        location=point_list[median][0],
        left_child=build_kdtree(point_list[:median], depth + 1),
        right_child=build_kdtree(point_list[median + 1:], depth + 1),
        key=point_list[median][1]
    )


def find_nearest_neighbor(coord, kdnode, depth=0):
    """
    Find the nearest neighboor to coord in the K-Depth Tree kdnode
    :param coord: (latitude, longitude)
    :param kdnode: KDNode. kdnode.location = (latitude, longitude)
    :param depth: The current depth in the tree. Determines which axis is used to organize and split the child nodes.
    :return: KDNode

    1. Find best leaf node. Save as current best.
    2. Unwind recursion up the tree:
    2.a. If current node is better, it becomes current best.
    2.b. Check the splitting plane for possibility of better node.
    2.b.i. If better node is possible, do the entire search on the subtree from current node.
    2.b.ii. Continue up the tree.
    """

    if kdnode is None:
        return None

    k = len(kdnode.location)  # assumes all points have the same dimension
    axis = depth % k
    nearest = None
    searched_left = None
    possible_nearest = None

    # What is center coord of axis? Difference with search coord determines direction
    # Tree is sorted low left to high right on axis?
    # 10 - 12 = -2, means go right
    # 14 - 8 = 6, means go left
    if kdnode.location[axis] - coord[axis] > 0:
        nearest = find_nearest_neighbor(coord, kdnode.left_child, depth + 1)
        searched_left = True
    else:
        nearest = find_nearest_neighbor(coord, kdnode.right_child, depth + 1)
        searched_left = False

    if nearest is None:
        return kdnode

    nearest_miles = geopy.distance.vincenty(coord, nearest.location).miles
    current_miles = geopy.distance.vincenty(coord, kdnode.location).miles

    if current_miles < nearest_miles:
        nearest = kdnode
        nearest_miles = current_miles

    # 2.b. Check the splitting plane for possibility of better node.
    # 2.b.i. If better node is possible, do the entire search on the subtree from current node.
    if abs(kdnode.location[axis] - coord[axis]) < abs(nearest.location[axis] - coord[axis]):
        if searched_left:
            possible_nearest = find_nearest_neighbor(coord, kdnode.left_child, depth + 1)
        else:
            possible_nearest = find_nearest_neighbor(coord, kdnode.right_child, depth + 1)

    if possible_nearest is None:
        return nearest

    if geopy.distance.vincenty(coord, possible_nearest.location).miles < nearest_miles:
        return possible_nearest

    return nearest


def main():
    """Example usage"""
    Point = namedtuple('Point', 'latitude longitude')
    KDItem = namedtuple('Item', 'point id')

    example_points = [KDItem(Point(2, 3), id=0), KDItem(Point(5, 4), id=1), KDItem(Point(9, 6), id=2),
                      KDItem(Point(4, 7), id=3), KDItem(Point(8, 1), id=4), KDItem(Point(7, 2), id=5)]
    # example_points = [((2, 3), 0), ((5, 4), 1), ((9, 6), 2), ((4, 7), 3), ((8, 1), 4), ((7, 2), 5)]

    tree = build_kdtree(example_points)

    print(tree)
    print(dir(tree))
    print(len(tree))
    print(tree[2])
    print(build_kdtree(example_points))


if __name__ == '__main__':
    main()
