import unittest
from numpy.testing import assert_allclose
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.beam import *


class TestBeam(unittest.TestCase):
    """
    Test Beam with Kneecap in the middle of the spam
    """
    def setUp(self):
        material = Material(E=2e6, f_y=1, f_u=1)
        section = Section(A=1, Ix=6e-3, material=material)
        node_1 = Node(0, no=1)
        node_2 = Node(5, no=2)
        node_3 = Node(10, no=3)
        member_1 = Member(node_1, node_2, section, (False, False), (False, True))
        member_2 = Member(node_2, node_3, section, (False, True), (False, False))
        member_1.forces = (2.5, Force(-10))
        member_2.distributed_loads = (0, DistributedForce(-10, -10, 5))
        node_1.restrains = (True, True)
        node_3.restrains = (True, True)
        self.beam = Beam()
        self.beam.members = [member_1, member_2]

    def test_action_result_vector(self):
        # Test Beam Problem
        self.beam.solve()
        k = [17.8125, 64.0625, 42.1875, -85.9375] 
        assert_allclose(self.beam.reactions, k)


if __name__ == '__main__':
    unittest.main()
