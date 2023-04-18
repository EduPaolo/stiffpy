"""
Module for Compression Design
    "*" Function arguments
    "-" Funtion Products
"""
import numpy as np


def flexional_buckling(K: float, member, L: float=member.length, method: str='LRFD'):
    """
    Flexional Buckling
    """
    r = np.array([member.section.rx, member.section.ry])
    slenderness = K*L/r
    euler_stress = np.pi**2*member.section.material.E/(slenderness)**2
    if slenderness <= 4.71*(member.section.material.E/member.section.material.f_y)**0.5:
        # Not long column
        buckling_stress = (0.658**(member.section.material.f_y/euler_stress))*member.section.material.f_y
    else:
        # Long Column
        buckling_stress = 0.877*euler_stress
    buckling_nominal_force = buckling_stress*member.section.A
    ultimate_buckling_force = 0.9*buckling_nominal_force if method == 'LRFD' else buckling_nominal_force/1.67


def torsional_buckling():
    """
    Torsional Buckling AISC E4
    """
    pass
