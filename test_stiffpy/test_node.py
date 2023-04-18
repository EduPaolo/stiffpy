import unittest
from numpy.testing import assert_almost_equal
from stiffpy.action.actions import Moment, Force
from stiffpy.node import Node

class TestAction(unittest.TestCase):
    def setUp(self):
        self.moment = Moment((4,5,6))
        self.force = Force((1,2,3))

    def test_node_properties(self):
        """
        Test Node Class Properties
        """
        node = Node((1,2,3))
        node.force, node.moment = self.force, self.moment
        node.restrains = (True, False, True, False, True, False)
        assert_almost_equal(node.action, [1,2,3,4,5,6])
        assert_almost_equal(node.restrains, [True, False, True, False, True, False])
    

if __name__ == '__main__':
    unittest.main()
