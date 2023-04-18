import unittest
import numpy as np
from numpy.testing import assert_allclose
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.truss import Node, Force, DistributedForce, Member, Moment, Truss


class TestTruss(unittest.TestCase):
    def setUp(self):
        material = Material(1, 1, 1)
        section = Section(2e5, 1, material=material)
        node_1 = Node((0, 3), no=1)
        node_2 = Node((4, 0), no=2)
        node_3 = Node((4, 3), no=3)
        node_4 = Node((8, 3), no=4)
        node_5 = Node((8, 0), no=5)
        node_6 = Node((12, 0), no=6)
        self.member_1 = Member(node_1, node_2, section)
        self.member_2 = Member(node_1, node_3, section)
        self.member_3 = Member(node_3, node_4, section)
        self.member_4 = Member(node_3, node_5, section)
        self.member_5 = Member(node_3, node_2, section)
        self.member_6 = Member(node_2, node_4, section)
        self.member_7 = Member(node_2, node_5, section)
        self.member_8 = Member(node_4, node_5, section)
        self.member_9 = Member(node_4, node_6, section)
        self.member_10 = Member(node_5, node_6, section)
        node_1.restrains = (True, True)
        node_2.restrains = (False, True)
        node_6.force = Force((0, -10))
        self.truss = Truss()
        self.truss.members = [
                self.member_1,
                self.member_2,
                self.member_3,
                self.member_4,
                self.member_5,
                self.member_6,
                self.member_7,
                self.member_8,
                self.member_9,
                self.member_10]
        self.truss.solve()

    def test_node_displacements(self):
        k = np.array([-0.1042E-02, 0.5333E-03, -0.6562E-04, 0.9500E-03, 
            -0.3046E-02, -0.1425E-02, -0.2981E-02, -0.1692E-02, -0.7263E-02])
        assert_allclose(self.truss.displacements, k, rtol=.02)

    def test_element_internal_actions(self):
        internal = []
        for member in self.truss.members:
            a = member.force_left.components[0]
            internal.append(-a)
        k = [-0.3333E+02, 0.2667E+02, 0.2083E+02, 0.7292E+01, -0.4375E+01,
                -0.9375E+01, -0.1917E+02, -0.4375E+01, 0.1667E+02, -0.1333E+02]
        assert_allclose(internal, k, rtol=.02)


if __name__ == '__main__':
    unittest.main()
