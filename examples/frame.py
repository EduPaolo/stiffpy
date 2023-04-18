from stiffpy.material import Material
from stiffpy.plotter.plotter_structure import PlotterStructure
from stiffpy.section import Section
from stiffpy.frame import *
from matplotlib import pyplot as plt


def main():
    # Define Section and Materials
    material = Material(E=2e7, f_y=1, f_u=1)
    section = Section(A=11.8*0.0254**2, Ix=518*0.0254**4, material=material)
    # Define nodes
    node_1 = Node((0, 0))
    node_2 = Node((0, 10))
    node_3 = Node((5, 10))
    node_4 = Node((10, 10))
    node_5 = Node((15, 5))
    node_6 = Node((5, 5))
    # Define members
    member_1 = Member(node_1, node_2, section)
    member_2 = Member(node_2, node_3, section)
    member_3 = Member(node_3, node_4, section)
    member_4 = Member(node_4, node_5, section)
    member_5 = Member(node_3, node_6, section)
    # Define Frame
    frame = Frame()
    # Add Member loads
    member_1.distributed_loads = (0, DistributedForce((0, -10), (0, -10), 10))
    member_2.distributed_loads = (0, DistributedForce((0, -10), (0, -10), 5))
    member_3.distributed_loads = (0, DistributedForce((0, -10), (0, -10), 5))
    member_4.distributed_loads = (0, DistributedForce((10/2**0.5, -10/2**0.5),
        (10/2**0.5, -10/2**0.5), 5*2**0.5))
    # Add node restrains
    node_1.restrains = (True, True, True)
    node_5.restrains = (True, True, True)
    node_6.restrains = (True, True, True)
    # Add members to frame object
    members = [member_1, member_2, member_3, member_4, member_5]
    frame.members = members
    # Solve
    frame.solve()
    print(frame.reactions)
    # Create plotter
    plotter = PlotterStructure(frame)
    # Create Axes and Figures
    _, axs = plt.subplots(2, 1)
    _, axs1 = plt.subplots(2, 1)
    # Draw Structure
    plotter.draw(axs[0])
    plotter.draw_deformated_shape(axs[1])
    # Draw Internal Actions
    member_1 = plotter.search_member(1)
    member_1.draw_shear_xy(axs1[0])
    member_1.draw_bending_xy(axs1[1])
    # Show figures
    plt.show()


if __name__ == '__main__':
    main()
