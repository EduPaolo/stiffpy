from ..node import Node
from ..member import Member
from ..section import Section


class Member(Member):
    def __init__(self, node_1: Node, node_2: Node, section: Section):
        super().__init__(
                node_1,
                node_2,
                section,
                node_1_release=(False, False, True, True, True, True),
                node_2_release=(False, False, True, True, True, True))
