import unittest
import numpy as np
from numpy.testing import assert_almost_equal
from stiffpy.section import Section
from stiffpy.material import Material
from stiffpy.node import Node
from stiffpy.member import Member

class TestMember(unittest.TestCase):
    def setUp(self):
        material = Material(1, 1, 1)
        section = Section(1, 1, material=material)
        # Beam Member Page 211 Matrix Analysis of Framed Structures
        self.beam_member = Member(
                Node((0, 0, 0), no=1),
                Node((10, 0, 0), no=2),
                section, 
                (True, False, True, True, True, False),
                (True, False, True, True, True, False))
        #  Truss
        self.truss_member = Member(
                Node((0, 0, 0), no=1),
                Node((6, 8, 0), no=2),
                section,
                (False, False, True, True, True, True),
                (False, False, True, True, True, True))
        #  Framed
        self.frame_member = Member(
                Node((0, 0, 0), no=1),
                Node((6, 8, 0), no=2),
                section,
                (False, False, True, True, True, False),
                (False, False, True, True, True, False))
        #  Space Truss
        self.space_truss_member = Member(
                Node((0, 0, 0), no=1),
                Node((3, 4, 5), no=2),
                section,
                (False, False, False, True, True, True),
                (False, False, False, True, True, True))
        #  Left Force-Free Beam
        self.force_left_beam = Member(
                Node((0, 0, 0), no=1),
                Node((10, 0, 0), no=2),
                section,
                (True, True, True, True, True, False),
                (True, False, True, True, True, False))
        # * Left Moment-Free Beam
        self.moment_left_beam = Member(
                Node((0, 0, 0), no=1),
                Node((10, 0, 0), no=2),
                section,
                (True, False, True, True, True, True),
                (True, False, True, True, True, False))
        # * Right Falseorce-Free Beam
        self.force_right_beam = Member(
                Node((0, 0, 0), no=1),
                Node((10, 0, 0), no=2),
                section,
                (True, False, True, True, True, False),
                (True, True, True, True, True, False))
        # * Right Moment-Free Beam
        self.moment_right_beam = Member(
                Node((0, 0, 0), no=1),
                Node((10, 0, 0), no=2),
                section,
                (True, False, True, True, True, False),
                (True, False, True, True, True, True))

    def test_member_oriented_stiffness_matrix(self):
        """
        Test Stiffness Member Matrix
        """
        k = np.array([
            [12, 60, -12, 60],
            [60, 400, -60, 200],
            [-12, -60, 12, -60],
            [60, 200, -60, 400]])/10**3
        assert_almost_equal(self.beam_member.member_oriented_stiffness_matrix, k)
        # Truss Member Length 10 Improvised
        k = np.array([
            [0.1, 0, -0.1, 0],
            [0, 0, 0, 0],
            [-0.1, 0, 0.1, 0],
            [0, 0, 0, 0]])
        assert_almost_equal(self.truss_member.member_oriented_stiffness_matrix, k)
        # Frame Member Length 10 Improvised
        k = np.array([
            [.1, 0, 0, -.1, 0, 0],
            [0, 12/1e3, 6/1e2, 0, -12/1e3, 6/1e2],
            [0, 6/1e2, .4, 0, -6/1e2, .2],
            [-.1, 0, 0, .1, 0, 0],
            [0, -12/1e3, -6/1e2, 0, 12/1e3, -6/1e2],
            [0, 6/1e2, .2, 0, -6/1e2, .4]
        ])
        assert_almost_equal(self.frame_member.member_oriented_stiffness_matrix, k)
        # Truss Space Member Length 5*2**0.5
        k = np.array([
            [0.14142135, 0, 0, -0.14142135, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [-0.14142135, 0, 0, 0.14142135, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ])
        assert_almost_equal(self.space_truss_member.member_oriented_stiffness_matrix, k)
        # Left Force-Free Beam
        k = np.array([
            [.1, 0, -.1],
            [0, 0, 0],
            [-.1, 0, .1]
        ])
        assert_almost_equal(self.force_left_beam.member_oriented_stiffness_matrix, k)
        # Left Moment-Free Beam
        k = np.array([
            [1, -1, 10],
            [-1, 1, -10],
            [10, -10, 100]
        ])*3/1e3
        assert_almost_equal(self.moment_left_beam.member_oriented_stiffness_matrix, k)
        # Right Force-Free Beam
        k = np.array([
            [0, 0, 0],
            [0, .1, -.1],
            [0, -.1, .1]
        ])
        assert_almost_equal(self.force_right_beam.member_oriented_stiffness_matrix, k)
        # Right Moment-Free Beam
        k = np.array([
            [1, 10, -1],
            [10, 100, -10],
            [-1, -10, 1]
        ])*3/1e3
        assert_almost_equal(self.moment_right_beam.member_oriented_stiffness_matrix, k)

    def test_member_rotation_matrix(self):
        # Truss
        k = np.array([
            [3/5, 4/5, 0, 0],
            [-4/5, 3/5, 0, 0],
            [0, 0, 3/5, 4/5],
            [0, 0, -4/5, 3/5]
        ])
        assert_almost_equal(self.truss_member.member_rotation_matrix, k)
        # Frame
        k = np.array([
            [3/5, 4/5, 0, 0, 0, 0],
            [-4/5, 3/5, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 3/5, 4/5, 0],
            [0, 0, 0, -4/5, 3/5, 0],
            [0, 0, 0, 0, 0, 1]
        ])
        assert_almost_equal(self.frame_member.member_rotation_matrix, k)


if __name__ == '__main__':
    unittest.main()
