""" Binary Search Tree ADT.
    Defines a Binary Search Tree with linked nodes.
    Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

from math import ceil
from typing import TypeVar, Generic
from node import TreeNode
import sys

# generic types
K = TypeVar('K')
I = TypeVar('I')
T = TypeVar('T')


class BinarySearchTree(Generic[K, I]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
            Initialises an empty Binary Search Tree
            :complexity: O(1)
        """

        self.root = None
        self.length = 0

    def is_empty(self) -> bool:
        """
            Checks to see if the bst is empty
            :complexity: O(1)
        """
        return self.root is None

    def __len__(self) -> int:
        """ Returns the number of nodes in the tree. """

        return self.length

    def __contains__(self, key: K) -> bool:
        """
            Checks to see if the key is in the BST
            :complexity: see __getitem__(self, key: K) -> (K, I)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: K) -> I:
        """
            Attempts to get an item in the tree, it uses the Key to attempt to find it
            :complexity best: O(CompK) finds the item in the root of the tree
            :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        return self.get_tree_node_by_key(key).item

    def get_tree_node_by_key(self, key: K) -> TreeNode:
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode:
        if current is None:
            raise KeyError('Key not found: {0}'.format(key))
        elif key == current.key:
            return current
        elif key < current.key:
            return self.get_tree_node_by_key_aux(current.left, key)
        else:  # key > current.key
            return self.get_tree_node_by_key_aux(current.right, key)

    def __setitem__(self, key: K, item: I) -> None:
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode:
        """
            Attempts to insert an item into the tree, it uses the Key to insert it
            :complexity best: O(CompK) inserts the item at the root.
            :complexity worst: O(CompK * D) inserting at the bottom of the tree
            where D is the depth of the tree
            CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: at the leaf
            current = TreeNode(key, item=item)
            current.subtree_size = 0
            self.length += 1
        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
        else:  # key == current.key
            raise ValueError('Inserting duplicate item')
        current.subtree_size += 1
        return current

    def __delitem__(self, key: K) -> None:
        self.root = self.delete_aux(self.root, key)

    def delete_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
            Attempts to delete an item from the tree, it uses the Key to
            determine the node to delete.
        """

        if current is None:  # key not found
            raise ValueError('Deleting non-existent item')
        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
        else:  # we found our key => do actual deletion
            if self.is_leaf(current):
                self.length -= 1
                return None
            elif current.left is None:
                self.length -= 1
                return current.right
            elif current.right is None:
                self.length -= 1
                return current.left

            # general case => find a successor
            succ = self.get_successor(current)
            current.key = succ.key
            current.item = succ.item
            current.right = self.delete_aux(current.right, succ.key)
        current.subtree_size -= 1
        return current

    def get_successor(self, current: TreeNode) -> TreeNode:
        """
            Get successor of the current node.
            It should be a child node having the smallest key among all the
            larger keys.

        - Args:
            - TreeNode: the node to be searched
        - Returns:
            - TreeNode | None: the child node having smallest key
        - Raises:
            -None
        - Complexity:
            O(D) where D is the maximum depth of given node
        """
        if self.is_leaf(current) or current.right is None:
            return None
        return self.get_minimal(current.right)

    def get_minimal(self, current: TreeNode) -> TreeNode:
        """
            Get a node having the smallest key in the current sub-tree.

        - Args:
            - TreeNode: current node
        - Returns:
            - TreeNode: the minimum node
        - Raises:
            -None
        - Complexity:
            O(D) where D is the maximum depth of given node
        """
        if self.is_leaf(current):
            return current
        return self.get_minimal(current.left)

    def is_leaf(self, current: TreeNode) -> bool:
        """ Simple check whether or not the node is a leaf. """

        return current.left is None and current.right is None

    def draw(self, to=sys.stdout):
        """ Draw the tree in the terminal. """

        # get the nodes of the graph to draw recursively
        self.draw_aux(self.root, prefix='', final='', to=to)

    def draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout) -> K:
        """ Draw a node and then its children. """

        if current is not None:
            real_prefix = prefix[:-2] + final
            print('{0}{1}'.format(real_prefix, str(current.key)), file=to)

            if current.left or current.right:
                self.draw_aux(current.left, prefix=prefix + '\u2551 ', final='\u255f\u2500', to=to)
                self.draw_aux(current.right, prefix=prefix + '  ', final='\u2559\u2500', to=to)
        else:
            real_prefix = prefix[:-2] + final
            print('{0}'.format(real_prefix), file=to)

    def kth_smallest(self, k: int, current: TreeNode) -> TreeNode:
        """
        Finds the kth smallest value by key in the subtree rooted at current.

        - Args:
            - TreeNode: current node
        - Returns:
            - TreeNode: the node which is k th smallest
        - Raises:
            -None
        - Complexity:
            O(D) where D is the maximum depth of given node
        """
        if current is None:
            return None

        left_size = current.left.subtree_size if current.left else 0

        if k == left_size + 1:
            return current
        elif k <= left_size:
            return self.kth_smallest(k, current.left)
        else:
            return self.kth_smallest(k - left_size - 1, current.right)

    def ratio(self, x: int, y: int) -> list[int]:
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
            O(logn + O) where n is the number of node and O is the length of return list
        """
        lb = ceil(x / 100 * self.length) + 1
        ub = self.length - ceil(y / 100 * self.length)
        lnode = self.kth_smallest(lb, self.root)
        unode = self.kth_smallest(ub, self.root)
        result = []
        self.ratio_helper(self.root, result, lnode, unode)
        return result

    def ratio_helper(self, current: TreeNode, result: list, x: TreeNode, y: TreeNode) -> None:
        """
        Helper function of ratio.

        - Args:
            - current: current node is processing
            - result: the list has to be return
            - x: the lower bound of all node
            - y: the upper bound of all node
        - Returns:
            - None
        - Raises:
            -None
        - Complexity:
            O(O) O is the length of return list
        """
        if current:
            if current is not x:
                self.ratio_helper(current.left, result, x, y)
            if x and y and x.item <= current.item <= y.item:
                result.append(current.key)
            if current is not y:
                self.ratio_helper(current.right, result, x, y)
