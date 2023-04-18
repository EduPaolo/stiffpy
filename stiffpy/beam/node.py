import numpy as np
from typing import Tuple
from ..node import Node as Node1


class Node(Node1):
    def __init__(self, r: float, no=None):
        super().__init__((r, 0, 0), no=no)

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
    def restrains(self, restrain: Tuple[bool, bool]):
        self._restrains = np.array([False, restrain[0], False, False, 
            False, restrain[1]])

    @elastic_constants.setter
    def elastic_constants(self, elastic_constant: list):
        self._elastic_constants = np.array([False, elastic_constant[0], 
            False, False, False, elastic_constant[1]])

    @displacements.setter
    def displacements(self, displacement: list):
        self._displacements = np.array([0, displacement[0], 0, 0, 
            0, displacement[1]])
