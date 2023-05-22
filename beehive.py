from dataclasses import dataclass
from heap import MaxHeap

@dataclass
class Beehive:
    """A beehive has a position in 3d space, and some stats."""

    x: int
    y: int
    z: int

    capacity: int
    nutrient_factor: int
    volume: int = 0

    def __init__(self, x, y ,z, capacity, nutrient_factor, volume):
        self.x = x
        self.y = y
        self.z = z
        self.capacity = capacity
        self.nutrient_factor = nutrient_factor
        self.volume = volume

    def __le__(self, other):
        """
        Comparison function less or equal
        Complexity: O(1)
        """
        return min(self.capacity, self.volume)*self.nutrient_factor <= min(other.capacity, other.volume)*other.nutrient_factor

    def __gt__(self, other):
        """
        Comparison function greater
        Complexity: O(1)
        """
        return min(self.capacity, self.volume)*self.nutrient_factor > min(other.capacity, other.volume)*other.nutrient_factor


class BeehiveSelector:

    def __init__(self, max_beehives: int):
        self.capacity = max_beehives
        self.store = MaxHeap(max_beehives)

    def set_all_beehives(self, hive_list: list[Beehive]):
        """
        Set all beehive into storage

        - Args:
            - list[Beehive]: a list of beehive to be stored
        - Returns:
            - None
        - Raises:
            -None
        - Complexity:
            O(n) where n is the length of given list of beehive
        """
        self.store = MaxHeap(self.capacity)
        self.store.heapify(hive_list) # O(n)

    def add_beehive(self, hive: Beehive):
        """
        Add given beehive into storage

        - Args:
            - Beehive: beehive to be stored
        - Returns:
            - None
        - Raises:
            -None
        - Complexity:
            O(log n) where n is the current length of self.store
        """
        self.store.add(hive)  # O(log n) :)
    
    def harvest_best_beehive(self):
        """
        Returns the value can be harvested.

        - Args:
            - None
        - Returns:
            - int: the total value harvested
        - Raises:
            -None
        - Complexity:
            O(n log n) where n is the current length of self.store
        """
        best: Beehive = self.store.get_max() # O(log n) :)
        value = min(best.capacity, best.volume)
        best.volume -= value
        self.store.add(best) # O(log n) :)
        return value * best.nutrient_factor
