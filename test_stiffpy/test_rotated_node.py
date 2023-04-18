import unittest
import numpy as np
from numpy.testing import assert_allclose
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.truss import Force, Member, Node, Truss


class TestTruss(unittest.TestCase):
    def setUp(self):
        material = Material(E=1, f_y=1, f_u=1)
        section = Section(A=1, Ix=1, material=material)
        node_1 = Node((4, 3), no=1)
        node_2 = Node((4, 0), angle=np.pi/4, no=2)
        node_3 = Node((0, 0), no=3)
        self.member_1 = Member(node_3, node_2, section)
        self.member_2 = Member(node_1, node_2, section)
        self.member_3 = Member(node_3, node_1, section)
        node_1.force = Force((30, 0))
        node_3.restrains = (True, True)
        node_2.restrains = (False, True)
        self.truss = Truss()
        self.truss.members = [self.member_1, self.member_2, self.member_3]
        self.truss.solve()

    def test_action_result_vector(self):
        # Test Truss Problem
        k = [31.81980515, -7.5, -22.5]
        assert_allclose(self.truss.reactions, k)


if __name__ == '__main__':
    unittest.main()
