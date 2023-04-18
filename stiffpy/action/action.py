import numpy as np
from typing import Tuple

from stiffpy.section import Section


class Action:
    """
    Generic Action Class. Due to the abstract nature of this class, it acts
    like an interface.

    Attributes
    ----------
    position: float
        Position, this attribute only works when the action is being aplicated
        in the member (not in the node)

    member_length: float
        Member length, this attribute only works when the action is being aplicated
        in the member (not in the node)

    initial_stiffness: np.ndarray
        Implements the stiffness matrix for a fixed member, this array will
        be use for the transformation of the action in the member into nodal
        actions
    """
    def __init__(self):
        pass

    @property
    def position(self):
        # Only for member loads 
        return self._position

    @property
    def member_length(self) -> float:
        # Only for member loads
        return self._member_length

    @property
    def member_section(self):
        # only for members loads
        return self._member_section

    @property
    def node_1_releases(self) -> Tuple[bool,bool,bool,bool,bool,bool]:
        # Only for member loads
        return self._node_1_releases

    @property
    def node_2_releases(self) -> Tuple[bool,bool,bool,bool,bool,bool]:
        # Only for member loads
        return self._node_2_releases

    @property
    def initial_stiffness(self):
        # Only for member loads
        e, g, a, ix, iy, j, l = self.member_section.material.E, \
                self.member_section.material.G, \
                self.member_section.A, \
                self.member_section.Ix, \
                self.member_section.Iy, \
                self.member_section.J, \
                self.member_length
        stiffness = np.zeros((12, 12))
        stiffness[[0,6],[0,6]], stiffness[6,0] = e*a/l, -e*a/l
        stiffness[[1,7],[1,7]], stiffness[7,1] = 12*e*ix/l**3, -12*e*ix/l**3
        stiffness[[2,8],[2,8]], stiffness[8,2] = 12*e*iy/l**3, -12*e*iy/l**3
        stiffness[[3,9],[3,9]], stiffness[9,3] = g*j/l, -g*j/l
        stiffness[[4,10],[4,10]] = 4*e*iy/l
        stiffness[[5,11],[5,11]] = 4*e*ix/l
        stiffness[[4,10],[2,2]], stiffness[[8,10],[4,8]] = -6*e*iy/l**2, 6*e*iy/l**2
        stiffness[[5,11],[1,1]], stiffness[[7,11],[5,7]] = 6*e*ix/l**2, -6*e*ix/l**2
        stiffness[10,4], stiffness[11,5] = 2*e*iy/l, 2*e*ix/l
        return stiffness + stiffness.T - np.diag(stiffness.diagonal())

    @member_length.setter
    def member_length(self, length: float):
        # Only for member loads
        self._member_length = length

    @member_section.setter
    def member_section(self, section: Section):
        # Only for member loads
        self._member_section = section

    @position.setter
    def position(self, location: float):
        # Only for member loads
        if location >= 0:
            self._position = location
        else:
            raise ValueError('Enter a positive location')

    @node_1_releases.setter
    def node_1_releases(self, release: Tuple[bool,bool,bool,bool,bool,bool]):
        # Only for member loads
        self._node_1_releases = release

    @node_2_releases.setter
    def node_2_releases(self, release: Tuple[bool,bool,bool,bool,bool,bool]):
        # Only for member loads
        self._node_2_releases = release
