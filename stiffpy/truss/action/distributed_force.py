from typing import Tuple
from ...action.distributed_force import DistributedForce as DF


class DistributedForce(DF):
    def __init__(self,
            inital_magnitude: Tuple[float, float],
            final_magnitude: Tuple[float, float],
            length: float):
        super().__init__(
                (inital_magnitude[0], inital_magnitude[1], 0),
                (final_magnitude[0], final_magnitude[1], 0),
                length)
