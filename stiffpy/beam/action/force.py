from ...action.actions import Force as Force1


class Force(Force1):
    def __init__(self, magnitude: float):
        super().__init__((0, magnitude, 0))
