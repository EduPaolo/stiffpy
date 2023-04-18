from ...action.distributed_force import DistributedForce as DF


class DistributedForce(DF):
    def __init__(self,
            inital_magnitude: float,
            final_magnitude: float,
            length: float):
        super().__init__((0, inital_magnitude, 0), (0, final_magnitude, 0), length)
