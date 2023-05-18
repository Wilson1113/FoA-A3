from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree

T = TypeVar("T")
I = TypeVar("I")

class Percentiles(Generic[T]):

    def __init__(self) -> None:
        self.store = list()

    def binary_search(self, item):
        lb = 0
        ub = len(self.store) - 1
        while lb <= ub:
            mid = (lb+ub)//2
            if self.store[mid] == item:
                return mid
            elif self.store[mid] > item:
                ub = mid - 1
            else:
                lb = mid + 1
        return lb
    
    def add_point(self, item: T):
        self.store.insert(self.binary_search(item),item)
    
    def remove_point(self, item: T):
        del self.store[self.binary_search(item)]

    def ratio(self, x, y):
        lb = ceil(x/100*len(self.store))
        ub = len(self.store) - ceil(y/100*len(self.store))
        return self.store[lb:ub]

if __name__ == "__main__":
    points = list(range(50))
    import random
    random.shuffle(points)
    p = Percentiles()
    for point in points:
        p.add_point(point)
    # Numbers from 8 to 16.
    print(p.ratio(15, 66))
