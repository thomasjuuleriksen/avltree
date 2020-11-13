class AVLNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.balance = 0

    def __repr__(self):
        if self.balance not in {-1, 0, 1}:
            raise ValueError("Tree invariant is broken")
        if self.left:
            left_val = self.left.value
        else:
            left_val = None
        if self.right:
            right_val = self.right.value
        else:
            right_val = None
        return f'<Node {self.value}>; balance={self.balance}; /' \
               f'(left tree top: {left_val}; right tree top: {right_val})'
