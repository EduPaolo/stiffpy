"""
Module for Traction Design
    "*" Function arguments
    "-" Funtion Products
"""


def yield_design(member, method: str='LRFD'):
    """
    Yield design of the member
        * member: Member object to design
        * method: LRFD or ASD
    """
    P_n = member.section.material.f_y*member.section.A
    if member == 'LRFD':
        P_u = P_n*0.9
    elif method == 'ASD':
        P_u == P_n/1.67
    else:
        raise TypeError('The Method is not valid')
    maximum_traction = member.axial_force[member.axial_force > 0].max()
    if maximum_traction/P_u < 1:
        return 'Accepted', maximum_traction, P_u
    else:
        return 'Rejected', maximum_traction, P_u
