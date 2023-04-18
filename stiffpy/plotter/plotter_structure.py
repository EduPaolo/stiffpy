from typing import List, Tuple

from stiffpy.plotter.plotter_node import PlotterNode
from stiffpy.plotter.plotter_member import PlotterMember
from ..member import Member
from ..structure import Structure
from matplotlib import pyplot as plt


class PlotterStructure:
    def __init__(self, structure: Structure) -> None:
        self.structure = structure
        # Create Plotter Node Objects
        self.nodes: List[PlotterNode] = []
        for node in self.structure.nodes:
            self.nodes.append(PlotterNode(node))
        # Create Plotter Member Objects
        self.members: List[PlotterMember] = []
        for member in self.structure.members:
            self.members.append(PlotterMember(member))

    def search_member(self, index: int=0) -> PlotterMember:
        return self.members[index]

    def draw(self, axs: plt.Axes):
        """
        Method to draw the entire structure
        """
        # Draw Members
        for member in self.members:
            member.draw(axs)
        # Draw Nodes
        for node in self.nodes:
            node.draw_node(axs)
        # Axes setup
        axs.set_title('Structure')
        axs.set_xlabel('X')
        axs.set_ylabel('Y')
        axs.grid()

    def draw_deformated_shape(self, axs: plt.Axes, factor: float=1):
        """
        Method to draw the deformated shape of the structure
        """
        # draw members
        for member in self.structure.members:
            deformed_shape = member.stacked_deformation*factor + member.global_domain
            axs.plot(
                    deformed_shape[0,...],
                    deformed_shape[1,...],
                    color='black')
        # draw nodes
        for node in self.nodes:
            node.draw_final_node(axs)
        axs.set_title('Structure')
        axs.set_xlabel('X')
        axs.set_ylabel('Y')
        axs.grid()
