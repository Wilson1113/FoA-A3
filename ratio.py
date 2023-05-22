from __future__ import annotations
from typing import Generic, TypeVar
from math import ceil
from bst import BinarySearchTree

T = TypeVar("T")
I = TypeVar("I")

class Percentiles(Generic[T]):

    def __init__(self) -> None:
        """
        List initialisation.

        - Args:
            - None
        - Returns:
            - None
        - Raises:
            -None
        - Complexity:
            O(1)
        """
        self.store = list()

    def binary_search(self, item):
        """
        Binary search function.

        - Args:
            - T: item to be search
        - Returns:
            - int: index to be insert or found
        - Raises:
            -None
        - Complexity:
            O(log n) where n is the length of self.store
        """
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
        """
        Function to add T into storage.

        - Args:
            - T: item to be added
        - Returns:
            - None
        - Raises:
            -None
        - Complexity:
            O(log n) where n is the length of self.store
        """
        self.store.insert(self.binary_search(item), item)
    
    def remove_point(self, item: T):
        """
        Function to remove T from storage.

        - Args:
            - T: item to be removed.
        - Returns:
            - None
        - Raises:
            -None
        - Complexity:
            O(log n) where n is the length of self.store
        """
        del self.store[self.binary_search(item)]

    def ratio(self, x, y):
        """
        Function returns the range of T with specific ratio.

        - Args:
            - int: specific the T has to be greater than x% amongst them
            - int: specific the T has to be less than y% amongst them
        - Returns:
            - list: element within the ratio
        - Raises:
            -None
        - Complexity:
            O(1)
        """
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
