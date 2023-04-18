"""
This module defines Material class, also defines 2 instances of this class
A36 and A572Grade50.

This module use Imperial Units (lbf, in, F)
"""

class Material:
    """
    Class to define new materials

    Attributes
    ----------
    f_y: float
        Yiels Stress (Fluencia)
    f_u: float
        Ultimate Stress (Ultimo)
    E: float
        Young Modulus
    v: float
        Poison Module
    w: float
        Density
    alpha: float
        Coefficient of thermal expansion 1/F
    """

    def __init__(self, f_y: float, f_u: float, E: float, v: float=0, w: float=0, alpha: float=0):
        """
        Material Class (lbf, in, F)

        Parameters
        ----------
        f_y: float
            Yiels Stress (Fluencia)
        f_u: float
            Ultimate Stress (Ultimo)
        E: float
            Young Modulus
        v: float
            Poison Module
        w: float
            Density
        alpha: float
            Coefficient of thermal expansion 1/F
        """    
        self.f_y = f_y
        self.f_u = f_u
        self.E = E
        self.v = v
        self.G = E/2/(1 + v)
        self.w = w
        self.alpha = alpha


A36 = Material(36e3, 58e3, 29e6, 0.3, 0.2836, 6.5e-6)
A572Grade50 = Material(50e3, 65e3, 29e3, 0.3, 0.2836, 6.5e-6)
