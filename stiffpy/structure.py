import matplotlib.pyplot as plt
import numpy as np
from typing import List, TypeVar
from .action.actions import Force, Moment
from .member import Member
from .node import Node


class Structure:
    def __init__(self):
        self._nodes = set()
        self._members: List[Member]

    @property
    def nodes(self):
        return list(self._nodes)

    @property
    def members(self) -> List[Member]:
        return self._members

    @property
    def indexes_grouped_by_node(self):
        """
        Nested List elements for each node e.g [[0,1,2],[3,4],[5..]
        """
        degrees_of_nodes: List[int] = [0]*len(self._nodes)
        sorted_node_list = sorted(self.nodes, key=lambda node: node.no)
        count = 0
        for node in sorted_node_list:
            no = node.no
            degrees_of_nodes[no-1] = [count + i for i in range(node.number_not_released)]
            count = degrees_of_nodes[no-1][-1] + 1
        return degrees_of_nodes

    @property
    def indexes(self):
        """
        Indexes of the whole structure
        """
        total_number_of_indexes = sum([node.number_not_released for node in self._nodes])
        return np.array([i for i in range(total_number_of_indexes)])

    @members.setter
    def members(self, members: List[Member]):
        for member in members:
            node_1, node_2 = member.node_1, member.node_2
            self._nodes.add(node_1)
            self._nodes.add(node_2)
        self._members = members

    @property
    def structure_stiffness(self):
        """
        The nodal and member releases could be different
        """
        indexes_grouped_by_node = self.indexes_grouped_by_node
        n = sum([node.number_not_released for node in self.nodes]) # Number of not released degrees of the entire structure
        stiffness = np.zeros((n, n))
        for member in self._members:
            pseudo_stiffness = np.zeros((n, n))
            Kuu = member.structure_oriented_stiffness_matrix[:member.node_1_number_not_released,:member.node_1_number_not_released]
            Kru = member.structure_oriented_stiffness_matrix[:member.node_1_number_not_released,member.node_1_number_not_released:]
            Kur = member.structure_oriented_stiffness_matrix[member.node_1_number_not_released:,:member.node_1_number_not_released]
            Krr = member.structure_oriented_stiffness_matrix[member.node_1_number_not_released:,member.node_1_number_not_released:]
            no_1, no_2 = member.node_1.no, member.node_2.no
            node_1_indexes = indexes_grouped_by_node[no_1-1] # Indexes corresponding to the node 1
            node_2_indexes = indexes_grouped_by_node[no_2-1] # Indexes corresponding to the node 2
            # selecting what indexes use
            node_1_not_released_indexes = [i for i, release in enumerate(member.node_1.release) if release == False]
            node_2_not_released_indexes = [i for i, release in enumerate(member.node_2.release) if release == False]
            node_1_bool_not_released = np.array(member.node_1.release)[node_1_not_released_indexes]
            node_2_bool_not_released = np.array(member.node_2.release)[node_2_not_released_indexes]
            member_node_1_bool_not_released = np.array(member.node_1_release)[node_1_not_released_indexes]
            member_node_2_bool_not_released = np.array(member.node_2_release)[node_2_not_released_indexes]
            node_1_bool = np.array([member_bool or nodal_bool for member_bool, nodal_bool in zip(member_node_1_bool_not_released, node_1_bool_not_released)])
            node_2_bool = np.array([member_bool or nodal_bool for member_bool, nodal_bool in zip(member_node_2_bool_not_released, node_2_bool_not_released)])
            node_1_indexes = np.array(node_1_indexes)[~node_1_bool]
            node_2_indexes = np.array(node_2_indexes)[~node_2_bool]
            pseudo_stiffness[np.stack(Kuu.shape[1]*[node_1_indexes],axis=1), np.stack(Kuu.shape[0]*[node_1_indexes],axis=0)] = Kuu
            pseudo_stiffness[np.stack(Kru.shape[1]*[node_1_indexes],axis=1), np.stack(Kru.shape[0]*[node_2_indexes],axis=0)] = Kru
            pseudo_stiffness[np.stack(Kur.shape[1]*[node_2_indexes],axis=1), np.stack(Kur.shape[0]*[node_1_indexes],axis=0)] = Kur
            pseudo_stiffness[np.stack(Krr.shape[1]*[node_2_indexes],axis=1), np.stack(Krr.shape[0]*[node_2_indexes],axis=0)] = Krr
            stiffness = stiffness + pseudo_stiffness
        return stiffness

    @property
    def elastic_constants(self):
        sorted_nodes = sorted(self._nodes, key=lambda node: node.no)
        return np.concatenate([node.elastic_constants[~np.array(node.release)] for node in sorted_nodes])

    @property
    def restrains(self):
        sorted_nodes = sorted(self._nodes, key=lambda node: node.no)
        return np.concatenate([node.restrains[~np.array(node.release)] for node in sorted_nodes])
    
    @property
    def nodal_actions(self):
        """
        Move from forces in a single member to forces in the whole structure
            - node_action: Action Vecto of the whole structure
            - no_list: 
        """
        n = sum([node.number_not_released for node in self.nodes])
        node_action = np.zeros(n)
        sorted_nodes = sorted(self.nodes, key=lambda node: node.no)
        for node in sorted_nodes:
            node_indexes = self.indexes_grouped_by_node[node.no-1]
            node_action[node_indexes] = node_action[node_indexes] + node.action[~np.array(node.release)]
        return node_action

    @property
    def member_load_actions(self):
        n = sum([node.number_not_released for node in self.nodes])
        member_load_action = np.zeros(n)
        for member in self.members:
            equivalent_joint_loads = member.structure_oriented_equivalent_joint_loads
            node_1_equivalent_joint_loads = equivalent_joint_loads[:member.node_1_number_not_released]
            node_2_equivalent_joint_loads = equivalent_joint_loads[member.node_1_number_not_released:]
            no_1, no_2 = member.node_1.no, member.node_2.no
            node_1_indexes = self.indexes_grouped_by_node[no_1-1]
            node_2_indexes = self.indexes_grouped_by_node[no_2-1]
            node_1_not_released_indexes = [i for i, release in enumerate(member.node_1.release) if release == False]
            node_2_not_released_indexes = [i for i, release in enumerate(member.node_2.release) if release == False]
            node_1_bool_not_released = np.array(member.node_1.release)[node_1_not_released_indexes]
            node_2_bool_not_released = np.array(member.node_2.release)[node_2_not_released_indexes]
            member_node_1_bool_not_released = np.array(member.node_1_release)[node_1_not_released_indexes]
            member_node_2_bool_not_released = np.array(member.node_2_release)[node_2_not_released_indexes]
            node_1_bool = np.array([member_bool or nodal_bool for member_bool, nodal_bool in zip(member_node_1_bool_not_released, node_1_bool_not_released)])
            node_2_bool = np.array([member_bool or nodal_bool for member_bool, nodal_bool in zip(member_node_2_bool_not_released, node_2_bool_not_released)])
            node_1_indexes = np.array(node_1_indexes)[~node_1_bool]
            node_2_indexes = np.array(node_2_indexes)[~node_2_bool]
            member_load_action[node_1_indexes] = member_load_action[node_1_indexes] + node_1_equivalent_joint_loads
            member_load_action[node_2_indexes] = member_load_action[node_2_indexes] + node_2_equivalent_joint_loads
        return member_load_action

    @property
    def displacements_effects(self):
        """
        Displacements effects in the nodes

        Notes
        -----
        Only works for displacements imposed at the supports, (does not work on
        unrestrained degrees).
        """
        n = sum([node.number_not_released for node in self.nodes])
        node_action = np.zeros(n)
        for member in self.members:
            equivalent_joint_loads = member.displacements_equivalent_joint_loads
            node_1_equivalent_joint_loads = \
                    equivalent_joint_loads[:member.node_1_number_not_released]
            node_2_equivalent_joint_loads = \
                    equivalent_joint_loads[member.node_1_number_not_released:]
            no_1, no_2 = member.node_1.no, member.node_2.no
            node_1_indexes = self.indexes_grouped_by_node[no_1-1]
            node_2_indexes = self.indexes_grouped_by_node[no_2-1]
            node_1_not_released_indexes = [i for i, release in 
                    enumerate(member.node_1.release) if release == False]
            node_2_not_released_indexes = [i for i, release in 
                    enumerate(member.node_2.release) if release == False]
            node_1_bool_not_released = np.array(member.node_1.release)\
                    [node_1_not_released_indexes]
            node_2_bool_not_released = np.array(member.node_2.release)\
                    [node_2_not_released_indexes]
            member_node_1_bool_not_released = np.array(member.node_1_release)\
                    [node_1_not_released_indexes]
            member_node_2_bool_not_released = np.array(member.node_2_release)\
                    [node_2_not_released_indexes]
            node_1_bool = np.array([member_bool or nodal_bool for member_bool,
                nodal_bool in zip(member_node_1_bool_not_released, 
                    node_1_bool_not_released)])
            node_2_bool = np.array([member_bool or nodal_bool for member_bool,
                nodal_bool in zip(member_node_2_bool_not_released, 
                    node_2_bool_not_released)])
            node_1_indexes = np.array(node_1_indexes)[~node_1_bool]
            node_2_indexes = np.array(node_2_indexes)[~node_2_bool]
            node_action[node_1_indexes] = node_action[node_1_indexes] + \
                    node_1_equivalent_joint_loads
            node_action[node_2_indexes] = node_action[node_2_indexes] + \
                    node_2_equivalent_joint_loads
        return node_action

    @property
    def number_of_degrees_of_freedom(self):
        """
        Number of degrees that has not been restrained
        """
        free_degrees = self.indexes[~self.restrains]
        return len(free_degrees)

    @property
    def reorder_indexes(self):
        """
        Free Degrees first and restrained degrees last
        """
        free_degrees = self.indexes[~self.restrains]
        restrained_degrees = self.indexes[self.restrains]
        return np.concatenate((free_degrees, restrained_degrees))

    @property
    def inverse_reorder_indexes(self):
        """
        Order of indexes to reverse the reorder_indexes
        """
        inverse_reorder_indexes = []
        for index in range(len(self.reorder_indexes)):
            for j, i in enumerate(self.reorder_indexes):
                if index == i:
                    inverse_reorder_indexes.append(j)
                    break
        return inverse_reorder_indexes

    def _redistribution(self):
        """
        Redistribute the displacements and the actions to their respective 
        node object
        """
        displacements_reorder_indexes = self.reorder_indexes[:self.number_of_degrees_of_freedom]
        actions_reorder_indexes = self.reorder_indexes[self.number_of_degrees_of_freedom:]
        for node in self._nodes:
            actions = []
            displacements = []
            elastic_actions = []
            new_actions = []
            new_displacements = []
            new_elastic_actions = []
            count = 0
            for index in displacements_reorder_indexes:
                # check if index correspond to the displacements index 
                if index in self.indexes_grouped_by_node[node.no-1]:
                    displacements.append(self.displacements[count])
                    elastic_actions.append(self.elastic_reactions[count])
                count = count + 1
            count = 0
            for index in actions_reorder_indexes:
                # check if index correspond to the displacements index 
                if index in self.indexes_grouped_by_node[node.no-1]:
                    actions.append(self.reactions[count])
                count = count + 1
            for restrain, release in zip(node.restrains, node.release):
                if restrain == False and release == False:
                    # if its a degree of freedom
                    new_actions.append(0)
                    new_displacements.append(displacements[0])
                    new_elastic_actions.append(elastic_actions[0])
                    displacements.pop(0)
                    elastic_actions.pop(0)
                elif restrain == False and release == True:
                    new_actions.append(0)
                    new_displacements.append(0)
                    new_elastic_actions.append(0)
                elif restrain == True and release == False:
                    new_actions.append(actions[0])
                    new_displacements.append(0)
                    new_elastic_actions.append(0)
                    actions.pop(0)
                elif restrain == True and release == True:
                    new_actions.append(0)
                    new_displacements.append(0)
                    new_elastic_actions.append(0)
            node.force = node.force + Force(new_actions[:3]) + Force(new_elastic_actions[:3])
            node.moment = node.moment + Moment(new_actions[3:]) + Moment(new_elastic_actions[3:])
            node._displacements = node._displacements + np.array(new_displacements)

    def _solve(self):
        self.action_combined = self.nodal_actions + self.member_load_actions + \
                self.displacements_effects
        # Action Vector
        self.reorder_action_combined = self.action_combined[self.reorder_indexes]
        # Stiffness Matrix
        effective_elastic_constants = self.elastic_constants[self.reorder_indexes]\
                [:self.number_of_degrees_of_freedom]
        new_structure_stiffness = self.structure_stiffness + np.diag(self.elastic_constants) # Elastic Support Effects
        self.reorder_stiffness = new_structure_stiffness[:, self.reorder_indexes][self.reorder_indexes, :]
        # Solving
        submatrix_to_solve = self.reorder_stiffness[:self.number_of_degrees_of_freedom,:self.number_of_degrees_of_freedom]
        subvector_to_solve = self.reorder_action_combined[:self.number_of_degrees_of_freedom]
        self.displacements = np.linalg.inv(submatrix_to_solve) @ subvector_to_solve
        self.reactions = -self.reorder_action_combined[self.number_of_degrees_of_freedom:] + self.reorder_stiffness[self.number_of_degrees_of_freedom:,:self.number_of_degrees_of_freedom] @ self.displacements
        self.elastic_reactions = -self.displacements * effective_elastic_constants

    def solve(self):
        self._solve()
        self._redistribution()
        for member in self.members:
            member._end_actions()
