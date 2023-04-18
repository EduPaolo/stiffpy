from typing import Tuple
from ...action.actions import Force as Force1


class Force(Force1):
    def __init__(self, components:Tuple[float, float]):
        super().__init__((components[0], components[1], 0))
