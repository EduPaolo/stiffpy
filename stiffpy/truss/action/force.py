from typing import Tuple
from ...action.actions import Force as F


class Force(F):
    def __init__(self, components: Tuple[float, float]):
        super().__init__((components[0], components[1], 0))
