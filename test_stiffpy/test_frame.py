import unittest
from numpy.testing import assert_allclose
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.frame import *


class TestFrame(unittest.TestCase):
    def setUp(self):
        material = Material(E=29e3, f_y=1, f_u=1)
        section = Section(A=10, Ix=500, Iy=500, material=material)
        node_1 = Node((0, 0), no=1)
        node_2 = Node((-20*12, 0), no=2)
        node_3 = Node((0, -20*12), no=3)
        member_1 = Member(node_2, node_1, section)
        member_2 = Member(node_1, node_3, section)
        node_1.force = Force((5, 0))
        node_3.restrains = (True, True, True)
        node_2.restrains = (False, True, False)
        self.frame = Frame()
        self.frame.members = [member_1, member_2]
        self.frame.solve()
        self.member_1 = member_1

    def test_action_result_vector(self):
        k = [-1.875, -5, 1.875, 750]
        assert_allclose(self.frame.reactions, k, rtol=.01, atol=.01)

    def test_displacements(self):
        k = [0.69575393, -0.00155071, -0.0024876, 0.69575393, 0.00123411]
        assert_allclose(self.frame.displacements, k, rtol=.01, atol=.01)

    def test_member_end_actions(self):
        # Member 1 choose for the testing
        force_left = [1.13801574e-13, -1.87378009e+00, 0.00000000e+00]  
        moment_left = [0, 0, 0.] 
        force_right = [-1.13801574e-13,  1.87378009e+00,  0.00000000e+00] 
        moment_right = [0, 0, -449.70722186]
        assert_allclose(self.member_1.force_left.components, force_left, rtol=.01, atol=.01)
        assert_allclose(self.member_1.moment_left.components, moment_left, rtol=.01, atol=.01)
        assert_allclose(self.member_1.force_right.components, force_right, rtol=.01, atol=.01)
        assert_allclose(self.member_1.moment_right.components, moment_right, rtol=.01, atol=.01)
        

if __name__ == '__main__':
    unittest.main()
