"""
Integrated Matrix Analysis of Structures, Mario Paz & William Leigh
Illustrative Example 6.1, pp 207
"""
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.truss import *


def main():
    # Define Material and Section
    material = Material(E=30e3, f_y=1, f_u=1)
    section = Section(A=10, Ix=882, material=material)
    # Define Nodes
    node_1 = Node((0, 0))
    node_2 = Node((100, 0))
    node_3 = Node((0, 100))
    # Define Members
    member_1 = Member(node_1, node_2, section)
    member_2 = Member(node_1, node_3, section)
    member_3 = Member(node_3, node_2, section)
    # Define Beam
    truss = Truss()
    # Add Node Loads
    node_3.force = Force((10, 0))
    # Add Restrains
    node_1.restrains = [True, True]
    node_2.restrains = [False, True]
    # Add Members to Beam Object
    members = [member_1, member_2, member_3]
    truss.members = members
    truss.solve()
    print(truss.reactions)


if __name__ == '__main__':
    main()
