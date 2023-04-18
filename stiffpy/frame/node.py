from typing import Tuple
import numpy as np
from ..node import Node as Node1


class Node(Node1):
    def __init__(self, r: Tuple[float, float], angle: float=0, no=None):
        super().__init__((r[0], r[1], 0), (0, 0, angle), no)

    @property
    def restrains(self):
        return self._restrains

    @property
    def elastic_constants(self):
        return self._elastic_constants

    @property
    def displacements(self):
        return self._displacements

    @restrains.setter
    def restrains(self, restrain: Tuple[bool, bool, bool]):
        self._restrains = np.array([restrain[0], restrain[1], False, False, False, restrain[2]])

    @elastic_constants.setter
    def elastic_constants(self, elastic_constant: list):
        self._elastic_constants = np.array([elastic_constant[0], elastic_constant[1], False, False, False, elastic_constant[2]])

    @displacements.setter
    def displacements(self, displacement: list):
        self._displacements = np.array([displacement[0], displacement[1], 0, 0, 0, displacement[2]])
