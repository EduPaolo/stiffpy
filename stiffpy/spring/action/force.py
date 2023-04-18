from ...action.actions import Force as Force1


class Force(Force1):
    def __init__(self, components: float):
        super().__init__((components, 0, 0))
