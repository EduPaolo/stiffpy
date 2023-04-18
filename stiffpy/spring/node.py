from typing import Tuple
import numpy as np
from ..node import Node as Node1


class Node(Node1):
    def __init__(self, r:float, no=None):
        super().__init__((r, 0, 0), (0, 0, 0), no)

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
    def restrains(self, restrain: bool):
        self._restrains = np.array([restrain, False, False, False, False, False])
