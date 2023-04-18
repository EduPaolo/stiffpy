from typing import Tuple
from ..member import Member as Member1
from ..node import Node
from ..section import Section

class Member(Member1):
    def __init__(self,
            node_1: Node,
            node_2: Node,
            section: Section,
            node1_release: Tuple[bool, bool, bool]=(False, False, False),
            node2_release: Tuple[bool, bool, bool]=(False, False, False)):
        super().__init__(
                node_1,
                node_2,
                section,
                node_1_release=(node1_release[0], node1_release[1], True, True, True, node1_release[2]),
                node_2_release=(node2_release[0], node2_release[1], True, True, True, node2_release[2]))
