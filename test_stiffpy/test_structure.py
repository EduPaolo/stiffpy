import unittest
import numpy as np
from numpy.testing import assert_allclose
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.action.actions import Moment, Force
from stiffpy.action.distributed_force import DistributedForce
from stiffpy.member import Member
from stiffpy.node import Node
from stiffpy.structure import Structure


class TestStructure(unittest.TestCase):
    def setUp(self):
        # Beam (Solution Manual Hibbeler problem 15-1)
        material = Material(1, 1, 1)
        section = Section(1, 1, material=material)
        node_1 = Node((0, 0, 0), no=1)
        node_2 = Node((6, 0, 0), no=2)
        node_3 = Node((10, 0, 0), no=3)
        member_1 = Member(
                node_1,
                node_2,
                section,
                (True, False, True, True, True, False),
                (True, False, True, True, True, False))
        member_2 = Member(
                node_2,
                node_3,
                section,
                (True, False, True, True, True, False),
                (True, False, True, True, True, False))
        member_1.distributed_loads = (0, DistributedForce((0, -25, 0), (0, -25, 0), 6))
        node_1.restrains = (False, True, False, False, False, True)
        node_2.restrains = (False, True, False, False, False, False)
        node_3.restrains = (False, True, False, False, False, True)
        self.beam = Structure()
        self.beam.members = [member_1, member_2]
        # Truss
        node_1 = Node((0, 0, 0), no=1)
        node_2 = Node((0, -3, 0), no=2)
        node_3 = Node((-4, -3, 0), no=3)
        node_4 = Node((-4, 0, 0), no=4)
        member_1 = Member(
                node_2,
                node_1,
                section,
                (False, False, True, True, True, True),
                (False, False, True, True, True, True))
        member_2 = Member(
                node_1,
                node_3,
                section,
                (False, False, True, True, True, True),
                (False, False, True, True, True, True))
        member_3 = Member(
                node_4,
                node_1,
                section,
                (False, False, True, True, True, True),
                (False, False, True, True, True, True))
        node_1.force = Force((0, -10, 0))
        node_2.restrains = (True, True, False, False, False, False)
        node_3.restrains = (True, True, False, False, False, False)
        node_4.restrains = (True, True, False, False, False, False)
        self.truss = Structure()
        self.truss.members = [member_1, member_2, member_3]
        # Frame (Estructural Analisis Hibbeler Page 623)
        material = Material(E=29e3, f_y=1, f_u=1)
        section = Section(A=10, Ix=500, Iy=500, material=material)
        node_1 = Node((0, 0, 0), no=1)
        node_2 = Node((-20*12, 0, 0), no=2)
        node_3 = Node((0, -20*12, 0), no=3)
        member_1 = Member(
                node_2,
                node_1,
                section,
                (False, False, True, True, True, False),
                (False, False, True, True, True, False))
        member_2 = Member(
                node_1,
                node_3,
                section,
                (False, False, True, True, True, False),
                (False, False, True, True, True, False))
        node_1.force = Force((5, 0, 0))
        node_2.restrains = (False, True, False, False, False, False)
        node_3.restrains = (True, True, False, False, False, True)
        self.frame = Structure()
        self.frame.members = [member_1, member_2]
        # Constrained Frame
        material = Material(E=2e7, f_y=1, f_u=1)
        section = Section(A=0.04, Ix=.2**4/12, material=material)
        node_1 = Node((0, 0, 0), no=1)
        node_2 = Node((0, 5, 0), no=2)
        node_3 = Node((5, 5, 0), no=3)
        node_4 = Node((5, 0, 0), no=4)
        member_1 = Member(
                node_1,
                node_2,
                section,
                (False, False, True, True, True, False),
                (False, False, True, True, True, False))
        member_2 = Member(
                node_2,
                node_3,
                section,
                (False, False, True, True, True, False),
                (False, False, True, True, True, False))
        member_3 = Member(
                node_3,
                node_4,
                section,
                (False, False, True, True, True, False),
                (False, False, True, True, True, False))
        member_4 = Member(
                node_1,
                node_3,
                section,
                (False, False, True, True, True, True),
                (False, False, True, True, True, True))
        member_5 = Member(
                node_4,
                node_2,
                section,
                (False, False, True, True, True, True),
                (False, False, True, True, True, True))
        node_2.force = Force((10, 0, 0))
        node_1.restrains = (True, True, False, False, False, False)
        node_4.restrains = (True, True, False, False, False, False)
        self.constrained_frame = Structure()
        self.constrained_frame.members = [member_1, member_2, member_3, member_4, member_5]

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
        # Test Beam Problem
        self.beam.solve()
        k = np.array([82.5, 90, 84.375, -16.875, 22.5])
        assert_allclose(self.beam.reactions, k, rtol=.01, atol=.01)
        # Test Truss Problem
        self.truss.solve()
        k = np.array([0, 8.75, 1.667, 1.25, -1.667, 0])
        assert_allclose(self.truss.reactions, k, rtol=.01, atol=.01)
        # Test Constrained Frame
        self.constrained_frame.solve()
        k = np.array([-4.423, -10, -5.577, 10])
        assert_allclose(self.constrained_frame.reactions, k, rtol=.01, atol=.01)
        # Test Frame Problem
        self.frame.solve()
        k = np.array([-1.875, -5, 1.875, 750])
        assert_allclose(self.frame.reactions, k, rtol=.01, atol=.01)


if __name__ == '__main__':
    unittest.main()
