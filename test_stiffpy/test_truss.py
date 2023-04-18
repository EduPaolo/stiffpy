import unittest
import numpy as np
from numpy.testing import assert_allclose
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.truss import Node, Force, DistributedForce, Member, Moment, Truss


class TestTruss(unittest.TestCase):
    def setUp(self):
        material = Material(1, 1, 1)
        section = Section(1, 1, material=material)
        node_1 = Node((0, 0), no=1)
        node_2 = Node((0, -3), no=2)
        node_3 = Node((-4, -3), no=3)
        node_4 = Node((-4, 0), no=4)
        self.member_1 = Member(node_2, node_1, section)
        self.member_2 = Member(node_1, node_3, section)
        self.member_3 = Member(node_4, node_1, section)
        node_1.force = Force((0, -10))
        node_2.restrains = (True, True)
        node_3.restrains = (True, True)
        node_4.restrains = (True, True)
        self.truss = Truss()
        self.truss.members = [self.member_1, self.member_2, self.member_3]

    def test_structure_stiffness_matrix(self):
        # Test Truss
        k = np.array([[.378, 0.096, 0, 0, -.128, -.096, -.25, 0],
            [.096, .405, 0, -0.3333, -0.096, -0.072, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, -.3333, 0, .3333, 0, 0, 0, 0],
            [-.128, -0.096, 0, 0, 0.128, 0.096, 0, 0],
            [-0.096, -0.072, 0, 0, .096, 0.072, 0, 0],
            [-.25, 0, 0, 0, 0, 0, .25, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]])
        assert_allclose(self.truss.structure_stiffness, k, rtol=.01, atol=.01)

    def test_action_result_vector(self):
        # Test Truss Problem
        self.truss.solve()
        k = np.array([0, 8.75, 1.667, 1.25, -1.667, 0])
        assert_allclose(self.truss.reactions, k, rtol=.01, atol=.01)


if __name__ == '__main__':
    unittest.main()
