import numpy as np
import math
from .material import Material, A36


class Section:
    def __init__(self, A, Ix, Iy=1, J=1, material=A36):
        """
        Custom section class
            * A: Area
            * Ix: Inertia around X axis
            * Iy: Inertia around Y axis
            * J: Torsion constant
            * material: Material of the section
        """
        self.A = A
        self.Ix = Ix
        self.Iy = Iy
        self.J = J
        self.material = material

    @property
    def rx(self):
        """
        Distribution of the cross-sectionanl area around its centroidal axis with the mass of the body
        """
        return math.sqrt(self.Ix/self.A)

    @property
    def ry(self):
        """
        Distribution of the cross-sectionanl area around its centroidal axis with the mass of the body
        """
        return math.sqrt(self.Iy/self.A)


class ISection(Section):
    def __init__(self, f1: float, ft1: float, f2: float, ft2: float, w: float, wt: float, material):
        """
        I section define
        The origin is at the bottom left corner of the section (the section only lay on the positive quadrant
            * f1: top flange width
            * ft1: to flange thickness
            * f2: bottom flange witdth
            * ft2: bottom flange thickness
            * w: web height
            * wt web thickness
        """
        self.f1 = f1
        self.f2 = f2
        self.ft1 = ft1
        self.ft2 = ft2
        self.w = w
        self.wt = wt
        self.height = self.ft1 + self.ft2 + self.w

    @property
    def A(self):
        """Area"""
        return self.f1*self.ft1 + self.f2*self.ft2 + self.w*self.wt

    @property
    def y_half(self):
        """Y half Equal Pieces distance"""
        x = (self.f2*self.ft2 - self.f1*self.ft1 + self.wt*self.w)/2/self.wt
        return self.ft2 + self.w - x

    @property
    def x_half(self):
        """X half equal pieces distance"""
        return max(self.f1, self.f2)/2

    @property
    def centroid(self):
        """Y Centroid"""
        first_term = self.f2*self.ft2*self.ft2/2 # Bottom Flange
        second_term = self.w*self.wt*(self.ft2 + self.w/2) # Web
        third_term = self.f1*self.ft1*(self.ft2 + self.w + self.ft1/2) # Upper Flange
        y_centroid = (first_term + second_term + third_term)/self.A 
        x_centroid = max(self.f1, self.f2)/2
        return np.array([x_centroid, y_centroid])

    @property
    def shear_centroid(self):
        """
        Shear Centroid, point where the loads shold pass if we don't want to generate torsion or other effects
        """
        return self.centroid

    @property
    def Ix(self):
        """Inertia around X Axis"""
        first_term = self.f2*self.ft2**3/12 + self.f2*self.ft2*(self.centroid[1] - self.ft2/2)**2 # Bottom Flange
        second_term = self.wt*self.w**3/12 + self.w*self.wt*(self.centroid[1] - self.ft2 - self.w/2)**2 # Web
        third_term = self.f1*self.ft1**3/12 + self.f1*self.ft1*(self.centroid[1] - self.ft2 - self.w - self.ft1/2)**2 # Top Flange
        return first_term + second_term + third_term

    @property
    def Iy(self):
        """Inertia around Y axis"""
        first_term = self.f2**3*self.ft2/12 # Bottom Flange
        second_term = self.wt**3*self.w/12 # Web
        third_term = self.f1**3*self.ft1/12 # Top Flange
        return first_term + second_term + third_term

    @property
    def J(self):
        """
        Torsion Constant
        Relation between angle of twist and the torque applied, only works on elastic range
        Only for ciicular cross section the J is the inertia normal to the section, for the others sections exists wrapping and we only can determine approximate solutions
        """
        d_prime = self.w + self.ft1 + self.ft2 - (self.ft1 + self.ft2)/2
        return (self.f1*self.ft1**3 + self.f2*self.ft2**3 + d_prime*self.wt**3)/3

    @property
    def Sx(self):
        """Elastic Section Modulus around X axis"""
        return self.Ix/max(self.centroid[1], self.w + self.ft1 + self.ft2 - self.centroid[1])

    @property
    def Sy(self):
        """Elastic Section Modulus around Y axis"""
        return self.Iy/self.centroid[0]

    @property
    def Zx(self):
        """Plastic Section Modulus around X axis"""
        first_term = self.ft1*self.f1*(self.height - self.y_half - self.ft1/2)
        second_term = self.ft2*self.f2*(self.y_half - self.ft2/2)
        third_term = self.wt*(self.wt + self.w - self.y_half)**2/2
        fourth_term = self.wt*(self.y_half - self.ft2)**2/2
        return first_term + second_term + third_term + fourth_term

    @property
    def Cw(self):
        """Warping Constant"""
        d_prime = self.height - (self.ft1 + self.ft2)/2
        alpha = 1/(1 + (self.f1/self.f2)**3*(self.ft1/self.ft2))
        return d_prime**2*self.f1**3*self.ft1*alpha/12


class TubeSection(Section):
    def __init__(self, f: float, ft: float, w: float, wt: float, material):
        """
        Tube Section class
            * f: flange width
            * ft: flange thickness
            * w: web hieght
            * wt web thickness
            * material: Material of the section
        """
        self.f = f
        self.ft = ft
        self.w = w
        self.wt = wt
        self.y_centroid, self.y_half = w/2, w/2
        self.x_centroid, self.x_half = f/2, f/2


    @property
    def A(self):
        return self.f*self.w - (self.f - 2*self.wt)*(self.w - 2*self.ft)


    @property
    def centroid(self):
        return np.array([self.f, self.w])/2


    @property
    def shear_centroid(self):
        return self.centroid


    @property
    def Ix(self):
        return self.f*self.w**3/12 - (self.f - 2*self.wt)*(self.w - 2*self.ft)**3/12


    @property
    def Iy(self):
        return self.w*self.f**3/12 - (self.w - 2*self.ft)*(self.f - 2*self.wt)**3/12

    
    @property
    def Sx(self):
        return self.Ix/self.w*2
    

    @property
    def Sy(self):
        return self.Iy/self.f*2


    @property
    def Zx(self):
        """Plastic Modulus around X axis"""
        prom = (self.ft + self.wt)/2
        return self.f*self.w**2/4 -(self.f - 2*prom)*(self.w/2 - prom)**2
