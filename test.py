import unittest
import random
from avltree import AVLTree


def check_invariant(tree):
    def calc_bal_and_inv(node):
        if node:
            left_ok, left_height = calc_bal_and_inv(node.left)
            right_ok, right_height = calc_bal_and_inv(node.right)
            if node.balance == 0:
                ok = (left_height == right_height)
            elif node.balance == -1:
                ok = left_height - 1 == right_height
            elif node.balance == 1:
                ok = left_height == right_height - 1
            else:
                raise ValueError(f"Invalid balance value at {node}!!")
            return (ok and left_ok and right_ok), (max(left_height, right_height) + 1)
        else:
            return True, 0

    if tree.head:
        avl_invariant_intact, _ = calc_bal_and_inv(tree.head)
        return avl_invariant_intact
    else:
        return True


class MyTestCase(unittest.TestCase):
    def test_insert_singlerotations(self):
        t = AVLTree(lambda x, y: x < y)
        l = [20, 10, 5, 80, 15, 100, 2, 1, 12, 11, 120, 0]
        for e in l:
            t.insert(e)
        expected_result_preorder = [10, 2, 1, 0, 5, 20, 12, 11, 15, 100, 80, 120]
        expected_result_inorder = [0, 1, 2, 5, 10, 11, 12, 15, 20, 80, 100, 120]
        expected_result_postorder = [0, 1, 5, 2, 11, 15, 12, 80, 120, 100, 20, 10]
        self.assertEqual(t.preorder(), expected_result_preorder)
        self.assertEqual(t.inorder(), expected_result_inorder)
        self.assertEqual(t.postorder(), expected_result_postorder)

    def test_insert_right_doublerotation_head_balanced(self):
        t = AVLTree(lambda x, y: x < y)
        l = [6, 8, 7]
        for e in l:
            t.insert(e)
        expected_preorder = [7, 6, 8]
        self.assertEqual(t.preorder(), expected_preorder)
        self.assertEqual(True, check_invariant(t))

    def test_insert_left_doublerotation_head_balanced(self):
        t = AVLTree(lambda x, y: x < y)
        l = [6, 4, 5]
        for e in l:
            t.insert(e)
        expected_preorder = [5, 4, 6]
        self.assertEqual(t.preorder(), expected_preorder)
        self.assertEqual(True, check_invariant(t))

    def test_insert_right_doublerotation_head_right_heavy(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100, 50, 200, 70, 150, 300, 120, 170, 250, 160]
        for e in l:
            t.insert(e)
        expected_preorder = [150, 100, 50, 70, 120, 200, 170, 160, 300, 250]
        self.assertEqual(t.preorder(), expected_preorder)
        self.assertEqual(True, check_invariant(t))

    def test_insert_left_doublerotation_head_left_heavy(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100, 50, 200, 30, 70, 150, 20, 60, 80, 90]
        for e in l:
            t.insert(e)
        expected_preorder = [70, 50, 30, 20, 60, 100, 80, 90, 200, 150]
        self.assertEqual(t.preorder(), expected_preorder)
        self.assertEqual(True, check_invariant(t))

    def test_insert_right_doublerotation_subtree_right_heavy(self):
        t = AVLTree(lambda x, y: x < y)
        l = [600, 200, 900, 150, 300, 800, 950, 120, 170, 250, 400, 700, 850, 920, 1000, 220, 270, 500, 230]
        for e in l:
            t.insert(e)
        expected_preorder = [600, 250, 200, 150, 120, 170, 220, 230, 300, 270, 400, 500, 900, 800, 700, 850, 950, 920, 1000]
        self.assertEqual(expected_preorder, t.preorder())
        self.assertEqual(True, check_invariant(t))

    def test_insert_left_doublerotation_subtree_left_heavy(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100, 50, 200, 30, 70, 150, 300, 20, 40, 60, 80, 120, 170, 250, 400, 110, 160, 180, 155]
        for e in l:
            t.insert(e)
        expected_preorder = [100, 50, 30, 20, 40, 70, 60, 80, 170, 150, 120, 110, 160, 155, 200, 180, 300, 250, 400]
        self.assertEqual(expected_preorder, t.preorder())
        self.assertEqual(True, check_invariant(t))

    def test_insert_dict_values(self):
        def less_than_func(d1, d2):
            return d1["year"] < d2["year"] or \
                (d1["year"] == d2["year"] and d1["month"] < d2["month"]) or \
                (d1["year"] == d2["year"] and d1["month"] == d2["month"] and d1["day"] < d2["day"]) or \
                (d1["year"] == d2["year"] and d1["month"] == d2["month"] and d1["day"] == d2["day"] and d1["pid"] < d2["pid"])

        t = AVLTree(less_than_func)
        p1 = {"Name": "Joe Brown", "Gender": "Male", "year": 1978, "month": 12, "day": 26, "pid": 7933}
        t.insert(p1)
        p2 = {"Name": "Charlotte Vest", "Gender": "Female", "year": 1979, "month": 12, "day": 26, "pid": 8712}
        t.insert(p2)
        p3 = {"Name": "Henning Primdahl", "Gender": "Male", "year": 1982, "month": 11, "day": 11, "pid": 2315}
        t.insert(p3)
        p4 = {"Name": "Robert Kock", "Gender": "Male", "year": 1976, "month": 12, "day": 26, "pid": 3771}
        t.insert(p4)
        p5 = {"Name": "Kate Bush", "Gender": "Female", "year": 1977, "month": 4, "day": 12, "pid": 9004}
        t.insert(p5)
        expected_preorder = [p2, p5, p4, p1, p3]
        self.assertEqual(expected_preorder, t.preorder())
        self.assertEqual(True, check_invariant(t))

    def test_insert_existing_values(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100, 50, 200, 30, 70, 150, 300, 20, 40, 60, 80, 120, 170, 250, 400, 110, 160, 180, 155]
        for e in l:
            t.insert(e)
        for e in l:
            t.insert(e)
        expected_preorder = [100, 50, 30, 20, 40, 70, 60, 80, 170, 150, 120, 110, 160, 155, 200, 180, 300, 250, 400]
        self.assertEqual(expected_preorder, t.preorder())
        self.assertEqual(True, check_invariant(t))

    def test_insert_large_tree(self):
        t = AVLTree(lambda x, y: x < y)
        l = random.sample(range(1000000000), 5000)
        avl_invariant_intact = True
        for e in l:
            t.insert(e)
            avl_invariant_intact = check_invariant(t) and avl_invariant_intact
        self.assertEqual(True, avl_invariant_intact)
        l.sort()
        self.assertEqual(l, t.inorder())

    def test_simple_delete_value_in_head_no_subtree(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100]
        for e in l:
            t.insert(e)
        t.delete(100)
        self.assertEqual((False, None), t.find(100))
        self.assertEqual(True, check_invariant(t))

    def test_simple_delete_value_in_leaf_no_rebalance(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100, 200, 50, 300, 20]
        for e in l:
            t.insert(e)
        t.delete(20)
        self.assertEqual((False, None), t.find(20))
        self.assertEqual(True, check_invariant(t))

    def test_delete_value_in_head_replace_w_leaf_node_no_rebalance(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100, 50, 150, 40, 60, 125, 160, 30, 55, 70, 180, 65, 80]
        for e in l:
            t.insert(e)
        t.delete(100)
        expected_preorder = [80, 50, 40, 30, 60, 55, 70, 65, 150, 125, 160, 180]
        self.assertEqual((False, None), t.find(100))
        self.assertEqual(expected_preorder, t.preorder())
        self.assertEqual(True, check_invariant(t))

    def test_delete_value_in_head_replace_w_subtree_node_no_rebalance(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100, 50, 150, 40, 60, 125, 160, 30, 55, 70, 180, 65]
        for e in l:
            t.insert(e)
        t.delete(100)
        expected_preorder = [70, 50, 40, 30, 60, 55, 65, 150, 125, 160, 180]
        self.assertEqual((False, None), t.find(100))
        self.assertEqual(expected_preorder, t.preorder())
        self.assertEqual(True, check_invariant(t))

    def test_delete_left_doublerotation_head_left_heavy(self):
        t = AVLTree(lambda x, y: x < y)
        l = [6, 2, 8, 3]
        for e in l:
            t.insert(e)
        t.delete(8)
        expected_preorder = [3, 2, 6]
        self.assertEqual((False, None), t.find(8))
        self.assertEqual(expected_preorder, t.preorder())
        self.assertEqual(True, check_invariant(t))

    def test_delete_right_doublerotation_head_left_heavy(self):
        t = AVLTree(lambda x, y: x < y)
        l = [6, 3, 8, 2, 5, 10, 4]
        for e in l:
            t.insert(e)
        t.delete(8)
        expected_preorder = [5, 3, 2, 4, 6, 10]
        self.assertEqual((False, None), t.find(8))
        self.assertEqual(expected_preorder, t.preorder())
        self.assertEqual(True, check_invariant(t))

    def test_delete_multiple_left_singlerotations(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100, 50, 500, 30, 70, 300, 700, 20, 40, 60, 80, 200, 400, 600, 10, 25, 35, 45, 55, 65, 150, 250, 5, 12]
        for e in l:
            t.insert(e)
        t.delete(600)
        expected_preorder = [50, 30, 20, 10, 5, 12, 25, 40, 35, 45, 100, 70, 60, 55, 65, 80, 300, 200, 150, 250, 500, 400, 700]
        self.assertEqual((False, None), t.find(600))
        self.assertEqual(expected_preorder, t.preorder())
        self.assertEqual(True, check_invariant(t))

    def test_delete_multiple_right_singlerotations(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100, 50, 500, 30, 70, 300, 700, 20, 40, 60, 80, 200, 400, 600, 900, 90, 350, 450, 550, 650, 850, 950, 925, 1000]
        for e in l:
            t.insert(e)
        t.delete(70)
        expected_preorder = [500, 100, 50, 30, 20, 40, 80, 60, 90, 300, 200, 400, 350, 450, 700, 600, 550, 650, 900, 850, 950, 925, 1000]
        self.assertEqual((False, None), t.find(70))
        self.assertEqual(expected_preorder, t.preorder())
        self.assertEqual(True, check_invariant(t))

    def test_delete_multiple_right_doublerotations(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100, 50, 500, 30, 70, 300, 700, 20, 40, 60, 80, 200, 400, 600, 900, 90, 350, 550, 650, 950, 625]
        for e in l:
            t.insert(e)
        t.delete(200)
        expected_preorder = [100, 50, 30, 20, 40, 70, 60, 80, 90, 600, 500, 350, 300, 400, 550, 700, 650, 625, 900, 950]
        self.assertEqual((False, None), t.find(200))
        self.assertEqual(expected_preorder, t.preorder())
        self.assertEqual(True, check_invariant(t))

    def test_delete_nonexistent_value_empty_tree(self):
        t = AVLTree(lambda x, y: x < y)
        with self.assertRaises(ValueError):
            t.delete(201)

    def test_delete_nonexistent_value_populated_tree(self):
        t = AVLTree(lambda x, y: x < y)
        l = [100, 50, 500, 30, 70, 300, 700, 20, 40, 60, 80, 200, 400, 600, 900, 90, 350, 550, 650, 950, 625]
        for e in l:
            t.insert(e)
        with self.assertRaises(ValueError):
            t.delete(201)

    def test_insert_large_tree_delete_all(self):
        t = AVLTree(lambda x, y: x < y)
        l = random.sample(range(1000000000), 5000)
        for e in l:
            t.insert(e)
        l.sort()
        avl_invariant_intact = True
        for e in l:
            t.delete(e)
            avl_invariant_intact = check_invariant(t) and avl_invariant_intact
        self.assertEqual(True, avl_invariant_intact)


if __name__ == '__main__':
    unittest.main()
