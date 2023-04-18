"""
Integrated Matrix Analysis of Structures, Mario Paz & William Leigh
Illustrative Example 1.4, pp 17
"""
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.beam import *
from stiffpy.plotter.plotter_structure import PlotterStructure
from matplotlib import pyplot as plt


def main():
    # Define Material and Section
    material = Material(E=29e3, f_y=1, f_u=1)
    section = Section(A=1, Ix=882, material=material)
    # Define Nodes
    node_1 = Node(0)
    node_2 = Node(90)
    node_3 = Node(180)
    node_4 = Node(300)
    node_5 = Node(396)
    # Define Members
    member_1 = Member(node_1, node_2, section)
    member_2 = Member(node_2, node_3, section)
    member_3 = Member(node_3, node_4, section)
    member_4 = Member(node_4, node_5, section)
    # Define Beam
    beam = Beam()
    # Add Node Loads
    node_2.force = Force(-10)
    node_3.moment = Moment(-50)
    # Add Member Loads
    member_1.forces = (10, Force(-30))
    member_1.forces = (20, Force(-10))
    member_2.distributed_loads = (0, DistributedForce(-.1, -.1, 90))
    member_3.distributed_loads = (20, DistributedForce(-.1, -.2, 75))
    member_4.distributed_loads = (0, DistributedForce(-.05, -.05, 96))
    member_4.moments = (48, Moment(100))
    # Add Restrains
    node_1.restrains = (True, True)
    node_3.restrains = (True, False)
    node_4.restrains = (True, False)
    node_5.restrains = (True, True)
    # Add Members to Beam Object
    members = [member_1, member_2, member_3, member_4]
    beam.members = members
    beam.solve()
    print(beam.reactions)
    # Draw Shear and Bending Diagrams
    plotter = PlotterStructure(beam)
    # Create Axes and Figures
    _, axs = plt.subplots(2, 1)
    # Create Axes
    plotter.draw(axs[0])
    plotter.draw_deformated_shape(axs[1])
    # Show Figures
    plt.show()


if __name__ == '__main__':
    main()
