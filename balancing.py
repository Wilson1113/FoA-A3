from __future__ import annotations
from threedeebeetree import Point
from ratio import Percentiles


def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    """
    Make the list into specific order which will make the tree be balanced

    - Args:
        - my_coordinate_list: A list contain all point
    - Returns:
        - result: A list contain all point in specific order
    - Raises:
        -None

    :complexity: O(N*logN) where N is the length of list
    """
    copy = sorted(my_coordinate_list)
    result = []
    make_ordering_aux(copy, result)  # O(n log n)
    return result


def make_ordering_aux(lst: list[Point], result: list[Point]) -> None:
    """
    The help function of make_ordering

    - Args:
        - lst: A list contain all point
        - result: The ordered list
    - Returns:
        - None
    - Raises:
        -None

    :complexity: O(N*logN) where N is the length of list
    """
    point = get_root(lst)  # n log n but n keep reducing in the process of recursive call
    # Check the list is empty so not is so stop recursive call
    # Not empty
    if lst:
        # If not point return for get_root add the leave point into result
        if point is None:
            for i in lst:
                result.append(i)
        # Else add the root into result and looking for 8 child node of this node
        else:
            result.append(point)

            child_list = split_list(lst, point)

            for sub_list in child_list:  # n log n/8 call
                make_ordering_aux(sub_list, result)


def get_root(copy: list[Point]) -> Point:
    """
    Get the root node key of this subtree

    - Args:
        - copy: A list contain all point
    - Returns:
        - pt: A point will be the root of this sublist (subtree)
    - Raises:
        -None

    :complexity: O(N*logN) where N is the length of list
    """
    # n log n
    # Create percentiles for using ratio
    p = Percentiles()
    py = Percentiles()
    pz = Percentiles()

    # Add all point into percentiles
    for i in copy:
        p.add_point(i)
        py.add_point(i[1])
        pz.add_point(i[2])

    # Find the "median" point of whole list
    lst = p.ratio(12.5, 12.5)
    lsty = py.ratio(12.5, 12.5)
    lstz = pz.ratio(12.5, 12.5)

    # Check the pt is in the "median" of y and z if so return it
    for pt in lst:
        if pt[1] in lsty and pt[2] in lstz:
            return pt


def split_list(lst, point: Point) -> list[list]:
    """
    Split one list into 8 sublist based on ggg, ggl, glg, gll, lgg, lgl, llg, lll compare to point.
    where g is greater l is less

    - Args:
        - point: point to compare
    - Returns:
        - result: list contain all sublist
    - Raises:
        -None

    :complexity: O(N) where N is the length of list
    """
    # list to store all sub list
    result = [[], [], [], [], [], [], [], []]

    # loop through all the point and based on compare function split them into 8 sublist
    for pt in lst:
        if pt != point:
            index = compare(point, pt)
            result[index].append(pt)
    return result


def compare(point1: Point, point2: Point) -> int:
    """
    Helper function determine the index after comparison

    - Args:
        - point1: point to compare
        - point2: point to compare
    - Returns:
        - int: index where should the point2 go if it is a child
    - Raises:
        -None
    - Complexity:
        O(1)
    """
    # Order: ggg, ggl, glg, gll, lgg, lgl, llg, lll
    result = 0
    # Case: l__
    result += int(point1[0] > point2[0]) << 2
    # Case: _l_
    result += int(point1[1] > point2[1]) << 1
    # Case: __l
    result += int(point1[2] > point2[2]) << 0
    return result
