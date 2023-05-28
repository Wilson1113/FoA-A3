from __future__ import annotations
from typing import Generic, TypeVar, Tuple
from dataclasses import dataclass, field

I = TypeVar('I')
Point = Tuple[int, int, int]


@dataclass
class BeeNode:
    key: Point
    item: I
    subtree_size: int = 1

    def __init__(self, key, item):
        self.key = key
        self.item = item
        # Order: ggg, ggl, glg, gll, lgg, lgl, llg, lll
        self.children = [None] * 8

    def get_child_for_key(self, point: Point) -> BeeNode | None:
        index = self.compare(point)
        return self.children[index]

    def compare(self, point2: Point) -> int:
        """
        Helper function determine the index after comparison

        - Args:
            - Point: point to compare
        - Returns:
            - int: index where should the point2 go if it is a child
        - Raises:
            -None
        - Complexity:
            O(1)
        """
        # Order: ggg, ggl, glg, gll, lgg, lgl, llg, lll
        # l__, _l_, __l
        return int(self.key[0] > point2[0]) << 2 + int(self.key[1] > point2[1]) << 1 + int(self.key[2] > point2[2]) << 0

class ThreeDeeBeeTree(Generic[I]):
    """ 3️⃣🇩🐝🌳 tree. """

    def __init__(self) -> None:
        """
            Initialises an empty 3DBT
        """
        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the 3DBT is empty
        """
        return len(self) == 0

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: Point) -> bool:
        """
            Checks to see if the key is in the 3DBT
        """
        try:
            self.get_tree_node_by_key(key)
            return True
        except KeyError:
            return False

    def __getitem__(self, key: Point) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
        """
        node = self.get_tree_node_by_key(key)
        return node.item

    def get_tree_node_by_key(self, key: Point) -> BeeNode:
        """
        Returns the child node where key = given key.

        - Args:
            - Point: key to search
        - Returns:
            - BeeNode: where key = given key
        - Raises:
            -KeyError: when key is not found in the tree
        - Complexity:
            O(D) where D is the maximum depth of root
        """
        current = self.root
        while current:
            if current.key == key:
                return current
            current = current.children[current.compare(key)]
        raise KeyError('Key not found!')

    def __setitem__(self, key: Point, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: BeeNode, key: Point, item: I) -> BeeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it

        - Args:
            - BeeNode: current root
            - Point: key to be inserted
            - I: item to be inserted
        - Returns:
            - BeeNode: the updated current
        - Raises:
            -None
        - Complexity:
            O(D) where D is the maximum depth of root
        """
        if not current:
            self.length += 1
            return BeeNode(key, item)
        elif current.key == key:
            current.item = item
            return current
        else:
            index = current.compare(key)
            current.children[index] = self.insert_aux(current.children[index], key, item)
            current.subtree_size = sum([child.subtree_size for child in current.children if child]) + 1  # O(1): always loop 8 times
            return current

    def is_leaf(self, current: BeeNode) -> bool:
        """
        Simple check whether or not the node is a leaf.

        - Args:
            - BeeNode: node to be checked
        - Returns:
            - bool: indicates whether given node is a leaf
        - Raises:
            -None
        - Complexity:
            O(1) we know it has maximum of 8 children
        """
        for child in current.children:
            if not child:
                return False
        return True


if __name__ == "__main__":
    tdbt = ThreeDeeBeeTree()
    tdbt[(3, 3, 3)] = "A"
    tdbt[(1, 5, 2)] = "B"
    tdbt[(4, 3, 1)] = "C"
    tdbt[(5, 4, 0)] = "D"
    print(tdbt.root.get_child_for_key((4, 3, 1)).subtree_size)  # 2
