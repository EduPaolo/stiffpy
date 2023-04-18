from ...action.actions import Moment


class Moment(Moment):
    def __init__(self, magnitude: float):
        super().__init__((0, 0, magnitude))
