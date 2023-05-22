from __future__ import annotations
from threedeebeetree import Point
from ratio import Percentiles


def make_ordering(my_coordinate_list: list[Point]) -> list[Point]:
    copy = sorted(my_coordinate_list)
    result = []
    make_ordering_aux(copy, result) # O(n log n)
    return result


def make_ordering_aux(lst, result):
    point = get_root(lst)
    if lst:
        if point is None:
            for i in lst:
                result.append(i)
        else:
            result.append(point)

            child_list = split_list(lst, point)

            for sub_list in child_list: # n log n/8 call
                make_ordering_aux(sub_list, result)


def get_root(copy):
    # n log n
    p = Percentiles()
    py = Percentiles()
    pz = Percentiles()

    for i in copy:
        p.add_point(i)
        py.add_point(i[1])
        pz.add_point(i[2])

    lst = p.ratio(12.5, 12.5)
    lsty = py.ratio(12.5, 12.5)
    lstz = pz.ratio(12.5, 12.5)

    for pt in lst:
        if pt[1] in lsty and pt[2] in lstz:
            return pt


def split_list(lst, point):
    result = [[], [], [], [], [], [], [], []]
    for pt in lst:
        if pt != point:
            index = compare(point, pt)
            result[index].append(pt)
    return result


def compare(point1: Point, point2: Point):
    # Order: ggg, ggl, glg, gll, lgg, lgl, llg, lll
    result = 0
    # Case: l__
    if point1[0] > point2[0]:
        result += 1 << 2
    # Case: _l_
    if point1[1] > point2[1]:
        result += 1 << 1
    # Case: __l
    if point1[2] > point2[2]:
        result += 1 << 0
    return result
