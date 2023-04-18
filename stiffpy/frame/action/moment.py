from ...action.actions import Moment as Moment1


class Moment(Moment1):
    def __init__(self, magnitude: float):
        super().__init__((0, 0, magnitude))
