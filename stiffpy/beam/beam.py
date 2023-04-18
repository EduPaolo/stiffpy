from ..structure import Structure
import numpy as np
from scipy.linalg import eigvals, eig


class Beam(Structure):
    def draw_deformations(self, factor=1):
        super().draw_deformations('2d', factor)

    def _stack_restrains(self) -> np.ndarray:
        # SetUp
        restrains_list = []
        # Sort Nodes
        order_nodes = sorted(list(self.nodes), key=lambda x: x.no)
        for node in order_nodes:
            restrains_list.extend(node.restrains[[1, 5]])
        return ~np.array(restrains_list)
