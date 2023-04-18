import numpy as np
from typing import Tuple
from .action.actions import Force, Moment
from scipy.spatial.transform import Rotation as R


class Node: 
    no = 1
    def __init__(self,
            r:Tuple[float,float,float],
            angle:Tuple[float,float,float]=(0, 0, 0),
            no=None):
        """
        Define the node number and the position list
            * no: Node number e.g: 1, 2, 3, ...
            * r: Position list e.g: [1, 2, 3]
            * angle: Rotation Angle radians
            - release: grades with releases, initial state is not released in any degree
            - restrains: Which degrees are restrained
            - default: if the releases are the default ones
        """
        self.no = Node.no if no == None else no
        Node.no += 1
        self.dimension = len(r)
        self.r = np.array(r)
        self.angle = np.array(angle)
        self.release = 6*[False]
        self._displacements: np.ndarray = np.array([0]*6)
        self._force = Force((0, 0, 0))
        self._moment = Moment((0, 0, 0))
        self._actions = np.array([*self._force.components, *self._moment.components])
        self._restrains = np.array([False]*6)
        self._elastic_constants = np.array([0]*6)
        self.default = True

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.no == other.no
        else:
            return False

    def __hash__(self):
        return hash(self.no)

    @property
    def r_f(self):
        return self.r + self.displacements[0:3]

    @property
    def force(self):
        return self._force

    @property
    def moment(self):
        return self._moment

    @property
    def action(self):
        return np.array([*self._force.components, *self._moment.components])

    @property
    def displacements(self):
        return self._displacements

    @property
    def elastic_constants(self):
        return self._elastic_constants

    @property
    def restrains(self):
        return self._restrains

    @force.setter
    def force(self, act: Force):
        """
        Set action
            * act: Force Action e.g: Force
        """
        self._force = act

    @elastic_constants.setter
    def elastic_constants(self, elastic_const):
        self._elastic_constants = np.array(elastic_const)

    @moment.setter
    def moment(self, act: Moment):
        """
        Set action
            * act: Moment Action e.g: Moment
        """
        self._moment = act

    @displacements.setter
    def displacements(self, displa: list):
        """
        Set displacements
            * displa: List of displacements at the node
        """
        self._displacements = np.array(displa)

    @restrains.setter
    def restrains(self, restrain: Tuple[bool,bool,bool,bool,bool,bool]):
        """
        Set Restrain in Joint
            * restrain: list of restrains according to type of structure. e.g: [True, False, True]
            (True means is restrained)
        """
        self._restrains = np.array(restrain)
        
    @property
    def number_not_released(self):
        return len(self.release) - sum(self.release)

    def compute_node_rotation_matrix(self, angle: np.ndarray):
        """
        Rotation matrix for the node
            angle: Array of Cosine angles of the member (radians)
        """
        effective_angle = np.array(angle)
        cosine_directors = np.cos(effective_angle)
        c_xz = np.sqrt(cosine_directors[0]**2 + cosine_directors[2]**2)
        if effective_angle[1] == 0 or effective_angle[1] == abs(np.pi):
            rotation_matrix = np.array([
                [0, cosine_directors[1], 0],
                [-cosine_directors[1], 0, 0],
                [0, 0, 1]
                ])
        else:
            rotation_matrix = np.array([
                [*cosine_directors],
                [-cosine_directors[1]*cosine_directors[0]/c_xz, c_xz, -cosine_directors[1]*cosine_directors[2]/c_xz],
                [-cosine_directors[2]/c_xz, 0, cosine_directors[0]/c_xz]
                ])
        r_member_angle = R.from_matrix(rotation_matrix)
        r_node_angle = R.from_rotvec(self.angle)
        rotation_matrix =  r_member_angle * r_node_angle
        return rotation_matrix.as_matrix()
