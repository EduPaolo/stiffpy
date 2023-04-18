import numpy as np
from stiffpy.material import Material
from ..member import Member as Member1
from ..node import Node
from ..section import Section

class Member(Member1):
    def __init__(self, node_1: Node, node_2: Node, k: float):
        material = Material(E=1, f_y=1, f_u=1)
        r_vector = node_2.r - node_1.r
        length = np.linalg.norm(r_vector)
        section = Section(A=k*length, Ix=1, material=material)
        super().__init__(node_1, node_2, section)
