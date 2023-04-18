"""
This module defines Member class

Member class is just an special type of Structure, we use this class to construct
more complex structures

This class has a similiar purpose to Plate or Membrane class

Notes
-----
Everything that starts with local or global are refering to the coordinates 
use to define that variable
"""

import numpy as np
from typing import Tuple
from scipy.linalg import block_diag
from .node import Node
from .section import Section
from .action.actions import Force, Moment
from .action.distributed_force import DistributedForce


class Member:
    def __init__(self,
            node_1: Node,
            node_2: Node,
            section: Section, 
            node_1_release: Tuple[bool,bool,bool,bool,bool,bool]=tuple(False for _ in range(6)),
            node_2_release: Tuple[bool,bool,bool,bool,bool,bool]=tuple(False for _ in range(6))):
        """
        Member class

        Parameters
        ----------
        node_1: Node
            Left node of the member
        node_2: Node
            Right node of the member
        section: Section 
            Section of the member
        node_1_release: Tuple, (False,False,False,False,False,False)
            member releases of the left node (not necesarily the same as 
            the node release), default not released
        node_2_release: Tuple, (False,False,False,False,False,False)
            member releases of the right node (not necesarily the same as 
            the node release), default not released
        """
        # check if the left and right node have the same dimension
        self.node_1 = node_1
        self.node_2 = node_2
        self.node_1_release = node_1_release
        self.node_2_release = node_2_release
        # Change nodes release according to member releases
        for i in range(len(node_1.release)):
            # Iterate over every release of the node 1
            if node_1.default == True:
                # Checks if its the first time we change the releases and 
                # if it change from False to True
                node_1.release[i] = node_1_release[i]
            elif node_1.release[i] == True and node_1_release[i] == False \
                    and node_1.default == False:
                # Cheks if its not the firs time we change the releases and 
                # if the release change from True to False
                node_1.release[i] = False
        for i in range(len(node_2.release)):
            # Iterate over every release of the node 2
            if node_2.default == True:
                # Checks if its the first time we change the releases and 
                # if it change from False to True
                node_2.release[i] = node_2_release[i]
            elif node_2.release[i] == True and node_2_release[i] == False \
                    and node_2.default == False:
                # Cheks if its not the firs time we change the releases and 
                # if the release change from True to False
                node_2.release[i] = False
        node_1.default = False
        node_2.default = False
        self.section = section
        r_vector = node_2.r - node_1.r
        self.length = float(np.linalg.norm(r_vector))
        self.angle = np.arccos(r_vector/self.length)
        self._forces = []
        self._moments = []
        self._distributed_loads = []
        # list of the indexes of the not released (release == False) of the left node
        self.node_1_index_not_released = [i for i, false in 
                enumerate(node_1_release) if false == False] 
        # list of the indexes of the not released (release == False) of the right node
        self.node_2_index_not_released = [i for i, false in 
                enumerate(node_2_release) if false == False] 
        self.node_1_number_not_released = len(node_1_release) - sum(node_1_release)
        self.node_2_number_not_released = len(node_2_release) - sum(node_2_release)
        self.domain = np.linspace(0, self.length, 1000)
        self.global_domain = (node_1.r + (np.linspace(0, 1, 1000)\
                [..., np.newaxis]*(node_2.r - node_1.r))).T

    @property
    def member_rotation_matrix(self):
        """
        Compute the member_rotation_matrix
        Note:
        The member rotation matrix R transforms matrices from global to local coordinates, if you want to tranforms something from local to global coordinates use its transpose R.T
            - node1_rotation_force: select the 3 first degrees of the node corresponding to force degrees
            - node2_rotation_force: select the 3 first degrees of the node corresponding to force degrees
            - node1_rotation_moment: select the 3 last degrees of the node corresponding to moment degrees
            - node2_rotation_moment: select the 3 last degrees of the node corresponding to moment degrees
            - node1_rotatioin_matrix_moment: compute the node rotatino matrix and according to node1_rotation_force select only the rows and columns to use
        """
        node1_rotation_force = ~np.array(self.node_1_release[:3])
        node1_rotation_moment = ~np.array(self.node_1_release[3:])
        node2_rotation_force = ~np.array(self.node_2_release[:3])
        node2_rotation_moment = ~np.array(self.node_2_release[3:])
        node1_rotation_matrix_force = self.node_1.compute_node_rotation_matrix(self.angle)[node1_rotation_force][:, node1_rotation_force]
        node1_rotation_matrix_moment = self.node_1.compute_node_rotation_matrix(self.angle)[node1_rotation_moment][:, node1_rotation_moment]
        node2_rotation_matrix_force = self.node_2.compute_node_rotation_matrix(self.angle)[node2_rotation_force][:, node2_rotation_force]
        node2_rotation_matrix_moment = self.node_2.compute_node_rotation_matrix(self.angle)[node2_rotation_moment][:, node2_rotation_moment]
        member_rotation = block_diag(
                node1_rotation_matrix_force,
                node1_rotation_matrix_moment,
                node2_rotation_matrix_force,
                node2_rotation_matrix_moment
                )
        return member_rotation

    @property
    def forces(self):
        return self._forces

    @property
    def moments(self):
        return self._moments

    @property
    def distributed_loads(self):
        return self._distributed_loads

    @property
    def member_oriented_stiffness_matrix(self):
        e, g, l, a, ix, iy, j = self.section.material.E, self.section.material.G, self.length, self.section.A, self.section.Ix, self.section.Iy, self.section.J
        stiffness = np.zeros((12, 12))
        stiffness[[0,6],[0,6]], stiffness[6,0] = e*a/l, -e*a/l
        stiffness[[1,7],[1,7]], stiffness[7,1] = 12*e*ix/l**3, -12*e*ix/l**3
        stiffness[[2,8],[2,8]], stiffness[8,2] = 12*e*iy/l**3, -12*e*iy/l**3
        stiffness[[3,9],[3,9]], stiffness[9,3] = g*j/l, -g*j/l
        stiffness[[4,10],[4,10]] = 4*e*iy/l
        stiffness[[5,11],[5,11]] = 4*e*ix/l
        stiffness[[4,10],[2,2]], stiffness[[8,10],[4,8]] = -6*e*iy/l**2, 6*e*iy/l**2
        stiffness[[5,11],[1,1]], stiffness[[7,11],[5,7]] = 6*e*ix/l**2, -6*e*ix/l**2
        stiffness[10,4], stiffness[11,5] = 2*e*iy/l, 2*e*ix/l
        stiffness = stiffness + stiffness.T - np.diag(stiffness.diagonal())
        merge_releases = np.array(self.node_1_release + self.node_2_release)
        matrix_release_rows = stiffness[merge_releases,:]
        matrix_release_rows_known, matrix_release_rows_unknown = matrix_release_rows[:,~merge_releases], matrix_release_rows[:, merge_releases]
        multiplication = -np.linalg.pinv(matrix_release_rows_unknown)@matrix_release_rows_known
        matrix_release_columns = stiffness[:, merge_releases]
        other_matrix_columns = stiffness[:, ~merge_releases]
        stiffness = (other_matrix_columns + matrix_release_columns @ multiplication)[~merge_releases,:]
        return stiffness

    @property
    def structure_oriented_stiffness_matrix(self):
        return self.member_rotation_matrix.T @ self.member_oriented_stiffness_matrix @ self.member_rotation_matrix

    @property
    def member_oriented_equivalent_joint_loads(self):
        cumulative_force_1 = Force((0, 0, 0))
        cumulative_force_2 = Force((0, 0, 0))
        cumulative_moment_1 = Moment((0, 0, 0))
        cumulative_moment_2 = Moment((0, 0, 0))
        for force in self.forces:
            # iterate over forces computing their the equivalent joint loads and sum it
            force_force_1, force_moment_1, force_force_2, force_moment_2 = force.compute_equivalent_joint_loads()
            cumulative_force_1 = cumulative_force_1 + force_force_1
            cumulative_force_2 = cumulative_force_2 + force_force_2
            cumulative_moment_1 = cumulative_moment_1 + force_moment_1
            cumulative_moment_2 = cumulative_moment_2 + force_moment_2
        for moment in self.moments:
            # iterate over moments computing their the equivalent joint loads and sum it
            moment_force_1, moment_moment_1, moment_force_2, moment_moment_2 = moment.compute_equivalent_joint_loads()
            cumulative_force_1 = cumulative_force_1 + moment_force_1
            cumulative_force_2 = cumulative_force_2 + moment_force_2
            cumulative_moment_1 = cumulative_moment_1 + moment_moment_1
            cumulative_moment_2 = cumulative_moment_2 + moment_moment_2
        for distri in self.distributed_loads:
            # iterate over distributed_forces computing their the equivalent joint loads and sum it
            distri_force_1, distri_moment_1, distri_force_2, distri_moment_2 = distri.compute_equivalent_joint_loads()
            cumulative_force_1 = cumulative_force_1 + distri_force_1
            cumulative_force_2 = cumulative_force_2 + distri_force_2
            cumulative_moment_1 = cumulative_moment_1 + distri_moment_1
            cumulative_moment_2 = cumulative_moment_2 + distri_moment_2
        # Internal end actions of the member
        self.force_left = Force(-cumulative_force_1.components)
        self.moment_left = Moment(-cumulative_moment_1.components)
        self.force_right = Force(-cumulative_force_2.components)
        self.moment_right = Moment(-cumulative_moment_2.components)
        return cumulative_force_1, cumulative_moment_1, cumulative_force_2, cumulative_moment_2

    @property
    def structure_oriented_equivalent_joint_loads(self):
        cumulative_force_1, cumulative_moment_1, cumulative_force_2, cumulative_moment_2 = self.member_oriented_equivalent_joint_loads
        combined_nodal1_actions = np.concatenate((cumulative_force_1.components, cumulative_moment_1.components))[~np.array(self.node_1_release)]
        combined_nodal2_actions = np.concatenate((cumulative_force_2.components, cumulative_moment_2.components))[~np.array(self.node_2_release)]
        return self.member_rotation_matrix.T @ np.array([*combined_nodal1_actions, *combined_nodal2_actions])

    @property
    def displacements_equivalent_joint_loads(self):
        """
        Actions due to imposed displacements at the nodes
        Note:
        Everything that starts with local or global are refering to the coordinates use for that variable
        """
        global_displacements = np.concatenate((self.node_1.displacements[~np.array(self.node_1_release)], self.node_2.displacements[~np.array(self.node_2_release)]))
        global_actions = -self.structure_oriented_stiffness_matrix @ global_displacements
        return global_actions

    @forces.setter
    def forces(self, location_force: Tuple[float, Force]):
        """
        Force setter method
            * location_force: (location, Force object)
        """
        force = location_force[1]
        force.position = location_force[0]
        force.member_length = self.length
        force.node_1_releases = self.node_1_release
        force.node_2_releases = self.node_2_release
        force.member_section = self.section
        self._forces.append(force)
    
    @moments.setter
    def moments(self, location_moment: Tuple[float, Moment]):
        """
        Momebt setter method
            * location_moment: [location, Moment object]
        """
        moment = location_moment[1]
        moment.position = location_moment[0]
        moment.member_length = self.length
        moment.node_1_releases = self.node_1_release
        moment.node_2_releases = self.node_2_release
        moment.member_section = self.section
        self._moments.append(moment)

    @distributed_loads.setter
    def distributed_loads(self, location_distri: Tuple[float, DistributedForce]):
        """
        Distributed Load setter method
            * location_force: [location, DistributedLoad object]
        """
        distri = location_distri[1]
        distri.position = location_distri[0]
        distri.member_length = self.length
        distri.node_1_releases = self.node_1_release
        distri.node_2_releases = self.node_2_release
        distri.member_section = self.section
        self._distributed_loads.append(distri)

    def _end_actions(self):
        actions = np.concatenate([self.force_left.components, self.moment_left.components, self.force_right.components, self.moment_right.components])
        actions = actions[~np.array(self.node_1_release + self.node_2_release)]
        displacements_1 = np.array(self.node_1.displacements)[~np.array(self.node_1_release)]
        displacements_2 = np.array(self.node_2.displacements)[~np.array(self.node_2_release)]
        displacements = np.concatenate([displacements_1, displacements_2])
        fem = (self.member_oriented_stiffness_matrix @ self.member_rotation_matrix) @ displacements + actions
        left_node_actions = fem[:self.node_1_number_not_released]
        right_node_actions = fem[self.node_1_number_not_released:]
        acts_left = []
        acts_right = []
        for release in self.node_1_release:
            if release == False:
                acts_left.append(left_node_actions[0])
                left_node_actions = np.delete(left_node_actions, 0)
            else:
                acts_left.append(0)
        for release in self.node_2_release:
            if release == False:
                acts_right.append(right_node_actions[0])
                right_node_actions = np.delete(right_node_actions, 0)
            else:
                acts_right.append(0)
        self.force_left = Force(acts_left[:3])
        self.moment_left = Moment(acts_left[3:])
        self.force_right = Force(acts_right[:3])
        self.moment_right = Moment(acts_right[3:])

    @property
    def axial_force(self):
        """
        Axial Force Vector along the member
        """
        initial_axial = -self.force_left.components[0]
        final_axial = self.force_right.components[0]
        axial_due_to_force = np.full_like(self.domain, initial_axial)
        for force in self.forces:
            temporary_axial_force = np.where(self.domain < force.position, 0, -force.components[0])
            axial_due_to_force = axial_due_to_force + temporary_axial_force
        for distributed_load in self.distributed_loads:
            temporary_axial_force = np.where(self.domain < distributed_load.position, 0, np.where(self.domain < distributed_load.position + distributed_load.length, -((distributed_load.initial_magnitudes[0] + np.interp(self.domain, [distributed_load.position, distributed_load.position + distributed_load.length], [distributed_load.initial_magnitudes[0], distributed_load.final_magnitudes[0]]))/2*(self.domain - distributed_load.position)), -((distributed_load.initial_magnitudes[0] + distributed_load.final_magnitudes[0])/2*distributed_load.length)))
            axial_due_to_force = axial_due_to_force + temporary_axial_force
        axial_due_to_force[-1] = final_axial
        return axial_due_to_force

    @property
    def torsion(self):
        """
        Torsion along the member
        """
        inital_torsion = -self.moment_left.components[0]
        final_torsion = self.moment_right.components[0]
        torsion_due_to_moment = np.full_like(self.domain, inital_torsion)
        for moment in self.moments:
            temporary_torsion = np.where(self.domain < moment.position, 0, -moment.components[0])
            torsion_due_to_moment = torsion_due_to_moment + temporary_torsion
        torsion_due_to_moment[-1] = final_torsion
        return torsion_due_to_moment

    @property
    def shear(self):
        """
        Shear along the member
        """
        initial_shear_xy = self.force_left.components[1]
        initial_shear_xz = self.force_left.components[2]
        final_shear_xy = -self.force_right.components[1]
        final_shear_xz = -self.force_right.components[2]
        shear_xy = np.full_like(self.domain, initial_shear_xy)
        shear_xz = np.full_like(self.domain, initial_shear_xz)
        for force in self.forces:
            temporary_shear_xy = np.where(self.domain < force.position, 0, force.components[1])
            temporary_shear_xz = np.where(self.domain < force.position, 0, force.components[2])
            shear_xy = shear_xy + temporary_shear_xy
            shear_xz = shear_xz + temporary_shear_xz
        for distributed_load in self.distributed_loads:
            temporary_shear_xy = np.where(
                    self.domain < distributed_load.position, 
                    0, 
                    np.where(
                        self.domain < distributed_load.position + distributed_load.length,
                        (distributed_load.initial_magnitudes[1] + np.interp(self.domain, [distributed_load.position, distributed_load.position], [distributed_load.initial_magnitudes[1], distributed_load.final_magnitudes[1]]))/2*(self.domain - distributed_load.position),
                        (distributed_load.initial_magnitudes[1] + distributed_load.final_magnitudes[1])/2*distributed_load.length
                        )
                    )
            temporary_shear_xz = np.where(
                    self.domain < distributed_load.position, 
                    0, 
                    np.where(
                        self.domain < distributed_load.position + distributed_load.length,
                        (distributed_load.initial_magnitudes[2] + np.interp(self.domain, [distributed_load.position, distributed_load.position], [distributed_load.initial_magnitudes[2], distributed_load.final_magnitudes[2]]))/2*(self.domain - distributed_load.position),
                        (distributed_load.initial_magnitudes[2] + distributed_load.final_magnitudes[2])/2*distributed_load.length
                        )
                    )
            shear_xy = shear_xy + temporary_shear_xy
            shear_xz = shear_xz + temporary_shear_xz
        shear_xy[-1] = final_shear_xy
        shear_xz[-1] = final_shear_xz
        return shear_xy, shear_xz

    @property
    def bending(self):
        """
        Bending Moment along the member
        """
        initial_shear_xy = self.force_left.components[1]
        initial_shear_xz = self.force_left.components[2]
        initial_bending_xy = -self.moment_left.components[2]
        initial_bending_xz = -self.moment_left.components[1]
        final_bending_xy = self.moment_right.components[2]
        final_bending_xz = self.moment_right.components[1]
        bending_xy = np.full_like(self.domain, initial_bending_xy)
        bending_xz = np.full_like(self.domain, initial_bending_xz)
        bending_xy = bending_xy + self.domain*initial_shear_xy
        bending_xz = bending_xz - self.domain*initial_shear_xz
        for moment in self.moments:
            temporary_bending_xy = np.where(self.domain < moment.position, 0, -moment.components[2])
            temporary_bending_xz = np.where(self.domain < moment.position, 0, moment.components[1])
            bending_xy = bending_xy + temporary_bending_xy
            bending_xz = bending_xz - temporary_bending_xz
        for force in self.forces:
            temporary_bending_xy = np.where(self.domain < force.position, 0, force.components[1]*(self.domain - force.position))
            temporary_bending_xz = -np.where(self.domain < force.position, 0, force.components[2]*(self.domain - force.position))
            bending_xy = bending_xy + temporary_bending_xy
            bending_xz = bending_xz + temporary_bending_xz
        for distributed_load in self.distributed_loads:
            temporary_bending_xz = np.where(
                    self.domain < distributed_load.position, 
                    0, 
                    np.where(
                        self.domain < distributed_load.position + distributed_load.length,
                        -(distributed_load.initial_magnitudes[2]*(self.domain - distributed_load.position))*(self.domain - distributed_load.position)/2 - ((np.interp(self.domain, [distributed_load.position, distributed_load.position + distributed_load.length], [distributed_load.initial_magnitudes[2], distributed_load.final_magnitudes[2]]) - distributed_load.initial_magnitudes[2])*(self.domain - distributed_load.position))/2*((self.domain - distributed_load.position)/3),
                        (distributed_load.initial_magnitudes[2]*(distributed_load.length))*(self.domain - (2*distributed_load.position + distributed_load.length)/2) + ((distributed_load.final_magnitudes[2] - distributed_load.initial_magnitudes[2])*(distributed_load.length))*(self.domain - (distributed_load.position + 2*(distributed_load.length)/3))
                        )
                    )
            temporary_bending_xy = np.where(
                    self.domain < distributed_load.position, 
                    0, 
                    np.where(
                        self.domain < distributed_load.position + distributed_load.length,
                        (distributed_load.initial_magnitudes[1]*(self.domain - distributed_load.position))*(self.domain - distributed_load.position)/2 + ((np.interp(self.domain, [distributed_load.position, distributed_load.position + distributed_load.length], [distributed_load.initial_magnitudes[1], distributed_load.final_magnitudes[1]]) - distributed_load.initial_magnitudes[1])*(self.domain - distributed_load.position))/2*((self.domain - distributed_load.position)/3),
                        -(distributed_load.initial_magnitudes[1]*(distributed_load.length))*(self.domain - (2*distributed_load.position + distributed_load.length)/2) - ((distributed_load.final_magnitudes[1] - distributed_load.initial_magnitudes[1])*(distributed_load.length))*(self.domain - (distributed_load.position + 2*(distributed_load.length)/3))
                        )
                    )
            bending_xy = bending_xy + temporary_bending_xy
            bending_xz = bending_xz + temporary_bending_xz
        bending_xy[-1] = final_bending_xy
        bending_xz[-1] = final_bending_xz
        return bending_xy, bending_xz

    @property
    def local_nodal_displacements(self):
        """
        Local Displacements for the nodes of the member
        """
        local_nodal_displacements = np.zeros(12)
        slice_global_nodal_displacements = np.concatenate((self.node_1.displacements[~np.array(self.node_1_release)], self.node_2.displacements[~np.array(self.node_2_release)]))
        slice_local_nodal_displacements = self.member_rotation_matrix @ slice_global_nodal_displacements
        local_nodal_displacements[np.concatenate((~np.array(self.node_1_release), ~np.array(self.node_2_release))).tolist()] = slice_local_nodal_displacements
        return local_nodal_displacements
        
    @property
    def slope(self):
        local_node_1_displacements = self.local_nodal_displacements[:6]
        local_node_2_displacements = self.local_nodal_displacements[6:]
        initial_slope_xy = local_node_1_displacements[5]
        initial_slope_xz = local_node_1_displacements[4]
        final_slope_xy = local_node_2_displacements[5]
        final_slope_xz = local_node_2_displacements[4]
        slope_xy = []
        slope_xz = []
        bending_xy, bending_xz = self.bending
        for i, _ in enumerate(self.domain):
            slope_in_a_point_xy = np.trapz(bending_xy[:i], self.domain[:i]) + initial_slope_xy*self.section.material.E*self.section.Ix
            slope_in_a_point_xz = np.trapz(bending_xz[:i], self.domain[:i]) + initial_slope_xy*self.section.material.E*self.section.Iy
            slope_xy.append(slope_in_a_point_xy)
            slope_xz.append(slope_in_a_point_xz)
        slope_xy[-1] = final_slope_xy*self.section.material.E*self.section.Ix
        slope_xz[-1] = final_slope_xz*self.section.material.E*self.section.Iy
        return np.array(slope_xy)/self.section.material.E/self.section.Ix, np.array(slope_xz)/self.section.material.E/self.section.Iy

    @property
    def deflection(self):
        local_node_1_displacements = self.local_nodal_displacements[:6]
        local_node_2_displacements = self.local_nodal_displacements[6:]
        initial_deflection_xy = local_node_1_displacements[1]
        initial_deflection_xz = local_node_1_displacements[2]
        final_deflection_xy = local_node_2_displacements[1]
        final_deflection_xz = local_node_2_displacements[2]
        deflection_xy = []
        deflection_xz = []
        slope_xy, slope_xz = self.slope
        for i, _ in enumerate(self.domain):
            deflection_in_a_point_xy = np.trapz(slope_xy[:i], self.domain[:i]) + initial_deflection_xy
            deflection_in_a_point_xz = np.trapz(slope_xz[:i], self.domain[:i]) + initial_deflection_xy
            deflection_xy.append(deflection_in_a_point_xy)
            deflection_xz.append(deflection_in_a_point_xz)
        deflection_xy[-1] = final_deflection_xy
        deflection_xz[-1] = final_deflection_xz
        return np.array(deflection_xy), np.array(deflection_xz)
        
    @property
    def axial_deformation(self):
        local_node_1_displacements = self.local_nodal_displacements[:6]
        local_node_2_displacements = self.local_nodal_displacements[6:]
        initial_deformation = local_node_1_displacements[0]
        final_deformation = local_node_2_displacements[0]
        deformation = []
        for i, _ in enumerate(self.domain):
            deformation_at_a_point = np.trapz(self.axial_force[:i], self.domain[:i]) + initial_deformation*self.section.A*self.section.material.E
            deformation.append(deformation_at_a_point)
        deformation[-1] = final_deformation*self.section.A*self.section.material.E
        return np.array(deformation)/self.section.A/self.section.material.E

    @property
    def stacked_deformation(self):
        """
        Mix all the deformations of the member in one array and transform it to global coordinates
        """
        deflection_xy, deflection_xz = self.deflection
        axial_deformation = self.axial_deformation
        local_stacked_deflections = np.stack((axial_deformation, deflection_xy, deflection_xz))
        effective_angle = np.array(self.angle) 
        cosine_directors = np.cos(effective_angle)
        c_xz = np.sqrt(cosine_directors[0]**2 + cosine_directors[2]**2)
        if effective_angle[1] == 0 or effective_angle[1] == abs(np.pi):
            rotation_matrix = np.array([[0, cosine_directors[1], 0], [-cosine_directors[1], 0, 0], [0, 0, 1]])
        else:
            rotation_matrix = np.array([[*cosine_directors], [-cosine_directors[1]*cosine_directors[0]/c_xz, c_xz, -cosine_directors[1]*cosine_directors[2]/c_xz], [-cosine_directors[2]/c_xz, 0, cosine_directors[0]/c_xz]])
        global_stacked_deflections = np.zeros_like(local_stacked_deflections)
        global_stacked_deflections = np.apply_along_axis(
                lambda x: x @ rotation_matrix,
                0,
                local_stacked_deflections)
        return global_stacked_deflections
