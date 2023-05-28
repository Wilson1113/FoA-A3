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
        self.store = BinarySearchTree()
    
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
        self.store[item] = item
    
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
        del self.store[item]

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
        return self.store.ratio(x,y)



if __name__ == "__main__":
    points = list(range(50))
    import random
    random.shuffle(points)
    p = Percentiles()
    for point in points:
        p.add_point(point)
    # Numbers from 8 to 16.
    print(p.ratio(15, 66))
