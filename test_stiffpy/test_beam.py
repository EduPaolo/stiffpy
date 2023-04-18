import unittest
import numpy as np
from numpy.testing import assert_allclose
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.beam import *


class TestBeam(unittest.TestCase):
    def setUp(self):
        # Beam (Solution Manual Hibbeler problem 15-1)
        material = Material(1, 1, 1)
        section = Section(1, 1, material=material)
        self.node_1 = Node(0, no=1)
        self.node_2 = Node(6, no=2)
        self.node_3 = Node(10, no=3)
        member_1 = Member(self.node_1, self.node_2, section)
        member_2 = Member(self.node_2, self.node_3, section)
        member_1.distributed_loads = (0, DistributedForce(-25, -25, 6))
        self.node_1.restrains = (True, True)
        self.node_2.restrains = (True, False)
        self.node_3.restrains = (True, True)
        self.beam = Beam()
        self.beam.members = [member_1, member_2]


    def test_structure_stiffness_matrix(self):
        # Test Beam
        k = np.array([
                [12/6**3, 1/6, -12/6**3, 1/6, 0, 0],
                [1/6, 2/3, -1/6, 1/3, 0, 0],
                [-12/6**3, -1/6, 12/4**3 + 12/6**3, -1/6 + .375, -.1875, .375],
                [1/6, 1/3, .375 - 1/6, 1 + 2/3, -.375, .5],
                [0, 0, -.1875, -.375, .1875, -.375],
                [0, 0, .375, .5, -.375, 1]
            ])
        assert_allclose(self.beam.structure_stiffness, k)
    

    def test_action_result_vector(self):
        # Test Beam Problem
        self.beam.solve()
        k = np.array([82.5, 90, 84.375, -16.875, 22.5])
        assert_allclose(self.beam.reactions, k, rtol=.01, atol=.01)


if __name__ == '__main__':
    unittest.main()
