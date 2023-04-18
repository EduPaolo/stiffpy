import unittest
import numpy as np
from numpy.testing import assert_almost_equal
from stiffpy.action.actions import Moment, Force
from stiffpy.action.distributed_force import DistributedForce
from stiffpy.member import Member
from stiffpy.node import Node
from stiffpy.section import Section
from stiffpy.material import Material

class TestAction(unittest.TestCase):
    def setUp(self):
        material = Material(1, 1, 1)
        self.section = Section(1, 1, material=material)
        self.node_1 = Node((0,0,0))
        self.node_2 = Node((1,0,0))
        self.moment = Moment((1, 1, 1))
        self.force = Force((1, 1, 1))
        self.distri = DistributedForce((0, 1, 1), (0, 2, 2), .2)

    def test_moment_equivalent_loads(self):
        """
        Test Moment equivalent joint loads for a fixed at left and right beam
        """
        member = Member(self.node_1, self.node_2, self.section)
        member.moments = (.3, self.moment)
        force_1, moment_1, force_2, moment_2 = member.member_oriented_equivalent_joint_loads
        assert_almost_equal(force_1.components, -np.array([0, 1.26, 1.26]), decimal=2)
        assert_almost_equal(moment_1.components,-np.array([0.7, -0.07, -0.07]), decimal=2)
        assert_almost_equal(force_2.components, -np.array([0, -1.26, -1.26]), decimal=2)
        assert_almost_equal(moment_2.components, -np.array([0.3, 0.33, 0.33]), decimal=2)
    
    def test_force_equivalent_loads(self):
        """
        Test Force equivalent joint loads for a fixed at left and right beam
        """
        member = Member(self.node_1, self.node_2, self.section)
        member.forces = (.3, self.force)
        force_1, moment_1, force_2, moment_2 = member.member_oriented_equivalent_joint_loads
        assert_almost_equal(force_1.components, -np.array([-.7, -.784, -.784]), decimal=2)
        assert_almost_equal(moment_1.components, -np.array([0, .147, -.147]), decimal=2)
        assert_almost_equal(force_2.components, -np.array([-.3, -.216, -.216]), decimal=2)
        assert_almost_equal(moment_2.components, -np.array([0, -0.06, 0.06]), decimal=2)

    def test_distributed_equivalent_loads(self):
        """
        Test Distributed Force equivalent joint loads for a fixed at left and right beam
        """
        member = Member(self.node_1, self.node_2, self.section)
        member.distributed_loads = (.3, self.distri)
        force_1, moment_1, force_2, moment_2 = member.member_oriented_equivalent_joint_loads
        assert_almost_equal(force_1.components, np.array([0, .19, .19]), decimal=2)
        assert_almost_equal(moment_1.components, np.array([0, -.04, .04]), decimal=2)
        assert_almost_equal(force_2.components, np.array([0, .11, .11]), decimal=2)
        assert_almost_equal(moment_2.components, np.array([0, 0.03, -0.03]), decimal=2)

    def test_distributed_equivalent_loads_articulated(self):
        """
        Test Distributed Force equivalent joint loads for a fixed at left and articulated at right beam
        """
        member = Member(
                self.node_1,
                self.node_2,
                self.section,
                node_1_release=(False,False,False,False,False,False),
                node_2_release=(False,False,False,False,True,True))
        member.distributed_loads = (.3, self.distri)
        force_1, moment_1, force_2, moment_2 = member.member_oriented_equivalent_joint_loads
        assert_almost_equal(force_1.components, np.array([0, .23, .23]), decimal=2)
        assert_almost_equal(moment_1.components, np.array([0, -.06, .06]), decimal=2)
        assert_almost_equal(force_2.components, np.array([0, .07, .07]), decimal=2)
        assert_almost_equal(moment_2.components, np.array([0, 0, 0]), decimal=2)


if __name__ == '__main__':
    unittest.main()
