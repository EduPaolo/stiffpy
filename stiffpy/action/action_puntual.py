import numpy as np
from typing import Tuple
from .action import Action


class ActionPuntual(Action):
    """ 
    Class that implements how a Puntual Action should behave

    Attributes
    ----------
    dimension: int
        Dimension
    components: np.ndarray
        Components of the Action
    magnitude: float
        Magnitude of the action
    """
    def __init__(self, components: Tuple[float, float, float]):
        """
        ActionPuntual implements the natural bahaviour of a Puntual
        Action

        Parameters
        ----------
        components: list 
            Components of the action, positive in the direction of X, Y,
            Z of the local axis.
        """
        self.components = np.array(components)
        self.magnitude = np.linalg.norm(self.components)

    def __str__(self):
        return f"ActionPuntual {self.components}"
