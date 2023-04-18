from typing import Tuple
from ..member import Member as Member1
from ..node import Node
from ..section import Section


class Member(Member1):
    def __init__(self,
            node_1: Node,
            node_2: Node,
            section: Section, 
            node1_release: Tuple[bool, bool]=(False, False),
            node2_release: Tuple[bool, bool]=(False, False)):
        super().__init__(
                node_1,
                node_2,
                section,
                (True, node1_release[0], True, True, True, node1_release[1]),
                (True, node2_release[0], True, True, True, node2_release[1]))
