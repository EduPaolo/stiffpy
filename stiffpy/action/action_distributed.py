from typing import Tuple
import numpy as np
from .action import Action


class ActionDistributed(Action):
    def __init__(self,
            initial_magnitudes: Tuple[float, float, float],
            final_magnitudes: Tuple[float, float, float],
            length: float):
        """
        Distributed Action Class

        Parameters
        ----------
        initial_magnitudes: Tuple
            Initial Magnitudes [init_x, init_y, init_z]
        final_magnitudes: Tuple
            Final Magnitudes [final_x, final_y, final_z]
        length: float
            Length of the distributed action
        """
        self.initial_magnitudes = np.array(initial_magnitudes)
        self.final_magnitudes = np.array(final_magnitudes)
        self.length = length

    @property
    def magnitudes(self):
        """
        Compute the magnitude of the distributed action
        """
        triangular_areas = (self.final_magnitudes - self.initial_magnitudes)*self.length/2
        rectangular_areas = self.initial_magnitudes*self.length
        return triangular_areas + rectangular_areas

    @property
    def centroids(self):
        """
        Compute centroid of the distributed action
        """
        triangular_areas = (self.final_magnitudes - self.initial_magnitudes)*self.length/2
        triangular_centroids = self.length*2/3
        rectangular_areas = self.initial_magnitudes*self.length
        rectangular_centroids = self.length/2

        # Formatting for nice output
        numerator = triangular_areas*triangular_centroids + \
                rectangular_areas*rectangular_centroids
        denominator = rectangular_areas + triangular_areas
        return numerator/denominator
