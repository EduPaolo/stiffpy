from matplotlib import pyplot as plt

from stiffpy.node import Node


class PlotterNode:
    def __init__(self, node: Node) -> None:
        self.node = node

    def draw_node(self, axs: plt.Axes):
        """
        Method to draw a Node in the Axes
        """
        # Draw Node
        axs.scatter(self.node.r[0], self.node.r[1])
        # Draw Node Label
        axs.annotate(
                text=self.node.no,
                xy=(self.node.r[0], self.node.r[1]))

    def draw_final_node(self, axs: plt.Axes):
        """
        Method to draw final position of the node
        """
        # Draw Node
        axs.scatter(self.node.r_f[0], self.node.r_f[1])
        # Draw Node Label
        axs.annotate(
                text=self.node.no,
                xy=(self.node.r_f[0], self.node.r_f[1]))
