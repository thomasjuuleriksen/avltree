"""
This module is a naive implementation of an AVL tree, which is a balanced binary tree,
cf. https://en.wikipedia.org/wiki/AVL_tree
"""

from node import AVLNode


class AVLTree:
    """
    The AVLTree class implements a number of methods on AVL trees, incl. the central methods:
    insert, delete and find, as well as methods for collapsing the tree in a list:
    preorder, inorder or postorder
    The remaining methods are auxiliary/internal and should not be used outside
    """
    def __init__(self, less_than_func):
        self.head = None
        self.less_than_func = less_than_func
        self.to_be_deleted_value_node = None
        self.inc = 0

    def adjust_pointers(self, parent_node, current_node, new_node):
        """
        Routine for finalising a rotation by fixing the rotated subtree on to the remaining tree
        :param parent_node: The node pointing to the rebalanced subtree
        :param current_node: The current subtree root node to be balanced down the subtree
        :param new_node: The new subtree root node
        :return: None
        """
        if parent_node.left == current_node:
            parent_node.left = new_node
        elif parent_node.right == current_node:
            parent_node.right = new_node
        else:
            self.head = new_node

    def singlerotation(self, parent_node, current_node, delete=False):
        # Move subtrees around
        if current_node.balance == -1:
            new_top_node = current_node.left
            current_node.left = new_top_node.right
            new_top_node.right = current_node
        else:
            new_top_node = current_node.right
            current_node.right = new_top_node.left
            new_top_node.left = current_node
        # Adjust balance values
        if delete and new_top_node.balance == 0:
            new_top_node.balance = -current_node.balance
            self.inc = 0
        else:
            current_node.balance = 0
            new_top_node.balance = 0
        # Adjust the pointer to the new top node
        self.adjust_pointers(parent_node, current_node, new_top_node)

    def doublerotation(self, parent_node, current_node):
        # Move subtrees around
        if current_node.balance == -1:
            new_top_node = current_node.left.right
            remain_node = current_node.left
            current_node.left.right = new_top_node.left
            new_top_node.left = current_node.left
            current_node.left = new_top_node.right
            new_top_node.right = current_node
        else:
            new_top_node = current_node.right.left
            remain_node = current_node.right
            current_node.right.left = new_top_node.right
            new_top_node.right = current_node.right
            current_node.right = new_top_node.left
            new_top_node.left = current_node
        # Adjust balance values
        if new_top_node.balance == current_node.balance:
            current_node.balance = -current_node.balance
            remain_node.balance = 0
        elif new_top_node.balance == 0:
            current_node.balance = 0
            remain_node.balance = 0
        elif new_top_node.balance == -current_node.balance:
            remain_node.balance = current_node.balance
            current_node.balance = 0
        else:
            raise ValueError("AVL invariance broken!!")
        new_top_node.balance = 0
        # Adjust the pointer to the new top node
        self.adjust_pointers(parent_node, current_node, new_top_node)

    def _find_parent(self, child_node):
        if child_node == self.head:
            return self.head
        candidate = self.head
        while True:
            if child_node in {candidate.left, candidate.right}:
                return candidate
            if self.less_than_func(child_node.value, candidate.value):
                candidate = candidate.left
            elif self.less_than_func(candidate.value, child_node.value):
                candidate = candidate.right

    def _iterative_insert(self, parent_node, current_node, value):
        place_found = False
        while not place_found:
            if self.less_than_func(value, current_node.value):
                if current_node.left:
                    parent_node = current_node
                    current_node = current_node.left
                else:
                    current_node.left = AVLNode(value)
                    self.inc = -1
                    place_found = True
            elif self.less_than_func(current_node.value, value):
                if current_node.right:
                    parent_node = current_node
                    current_node = current_node.right
                else:
                    current_node.right = AVLNode(value)
                    self.inc = 1
                    place_found = True
            else:  # value equal to current_node.value; value shall be ignored
                self.inc = 0
                place_found = True
        while self.inc != 0:
            # height of subtree changed
            if current_node.balance == 0:
                current_node.balance = self.inc
                if current_node == parent_node.left:
                    self.inc = -abs(self.inc)
                else:
                    self.inc = abs(self.inc)
            elif current_node.balance == -self.inc:
                current_node.balance = 0
                self.inc = 0
            elif current_node.balance == self.inc:
                if (self.inc == -1 and current_node.left.balance == -current_node.balance) or \
                        (self.inc == 1 and current_node.right.balance == -current_node.balance):
                    self.doublerotation(parent_node, current_node)
                else:
                    self.singlerotation(parent_node, current_node)
                self.inc = 0
            if current_node == self.head:
                break
            current_node = parent_node
            parent_node = self._find_parent(parent_node)

    def _recursive_insert(self, parent_node, current_node, value):
        # Find the right place in the tree to insert the new value
        if self.less_than_func(value, current_node.value):
            if current_node.left:
                self._recursive_insert(current_node, current_node.left, value)
                self.inc = -abs(self.inc)
            else:
                current_node.left = AVLNode(value)
                self.inc = -1
        elif self.less_than_func(current_node.value, value):
            if current_node.right:
                self._recursive_insert(current_node, current_node.right, value)
                self.inc = abs(self.inc)
            else:
                current_node.right = AVLNode(value)
                self.inc = 1
        else:  # value exists already (equal to current_node.value); value shall be ignored
            self.inc = 0
        # If needed, re-balance the tree
        if self.inc != 0:
            if current_node.balance == 0:
                current_node.balance = self.inc
            elif current_node.balance == -self.inc:
                current_node.balance = 0
                self.inc = 0
            elif current_node.balance == self.inc:
                if (self.inc == -1 and current_node.left.balance == -current_node.balance) or \
                        (self.inc == 1 and current_node.right.balance == -current_node.balance):
                    self.doublerotation(parent_node, current_node)
                else:
                    self.singlerotation(parent_node, current_node)
                self.inc = 0

    def insert(self, value):
        if not self.head:
            self.head = AVLNode(value)
        else:
            self._iterative_insert(self.head, self.head, value)

    def _recursive_delete(self, parent_node, current_node, value):
        if self.to_be_deleted_value_node:  # Value to be deleted found further up in the tree
            if current_node.right:
                self._recursive_delete(current_node, current_node.right, value)
                self.inc = -abs(self.inc)
            else:
                self.to_be_deleted_value_node.value = current_node.value
                if parent_node.left == current_node:
                    self.inc = 1
                elif parent_node.right == current_node:
                    self.inc = -1
                self.adjust_pointers(parent_node, current_node, current_node.left)
                return  # No need to re-balance the potential subtree of the deleted node
        else:
            if current_node:
                if self.less_than_func(value, current_node.value):
                    self._recursive_delete(current_node, current_node.left, value)
                    self.inc = abs(self.inc)
                elif self.less_than_func(current_node.value, value):
                    self._recursive_delete(current_node, current_node.right, value)
                    self.inc = -abs(self.inc)
                else:
                    self.to_be_deleted_value_node = current_node  # Value to be deleted is current node
                    if not current_node.left:
                        if parent_node.left == current_node:
                            self.inc = 1
                        elif parent_node.right == current_node:
                            self.inc = -1
                        self.adjust_pointers(parent_node, current_node, current_node.right)
                        return  # No need to re-balance the potential subtree of the deleted node
                    self._recursive_delete(current_node, current_node.left, value)
                    self.inc = abs(self.inc)
            else:
                raise ValueError(f"{value} not found in tree!")
        if self.inc != 0:
            # If needed, re-balance the tree
            if current_node.balance == 0:
                current_node.balance = self.inc
                self.inc = 0
            elif current_node.balance == -self.inc:
                current_node.balance = 0
                self.inc = -1
            elif current_node.balance == self.inc:
                if (self.inc == -1 and current_node.left.balance == -current_node.balance) or \
                        (self.inc == 1 and current_node.right.balance == -current_node.balance):
                    self.doublerotation(parent_node, current_node)
                    self.inc = -1
                else:
                    self.singlerotation(parent_node, current_node, delete=True)

    def delete(self, value):
        if not self.head:
            raise ValueError("Trying to delete from an empty tree!")
        self.to_be_deleted_value_node = None
        self._recursive_delete(self.head, self.head, value)

    def _recursive_find(self, current_node, value):
        if current_node:
            if self.less_than_func(value, current_node.value):
                return self._recursive_find(current_node.left, value)
            if self.less_than_func(current_node.value, value):
                return self._recursive_find(current_node.right, value)
            return True, current_node
        return False, None

    def find(self, value):
        if self.head:
            return self._recursive_find(self.head, value)
        return False, None

    def inorder(self):
        def _inorder_rec(node):
            if node:
                return _inorder_rec(node.left) + [node.value] + _inorder_rec(node.right)
            return []
        return _inorder_rec(self.head)

    def preorder(self):
        def _preorder_rec(node):
            if node:
                return [node.value] + _preorder_rec(node.left) + _preorder_rec(node.right)
            return []
        return _preorder_rec(self.head)

    def postorder(self):
        def _postorder_rec(node):
            if node:
                return _postorder_rec(node.left) + _postorder_rec(node.right) + [node.value]
            return []
        return _postorder_rec(self.head)
