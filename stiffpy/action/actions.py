from typing import Tuple
import numpy as np
from .action_puntual import ActionPuntual


class Force(ActionPuntual):
    def __init__(self, components: Tuple[float, float, float]):
        super().__init__(components)

    def __add__(self, other):
        if isinstance(other, Force):
            return Force((self.components + other.components).tolist())
        else:
            raise TypeError('You cannot add different types of Actions')

    def compute_equivalent_joint_loads(self):
        """
        Equivalent Joint Loads for Forces 
        """
        # Reassingning variables (easy to handle)
        a = self.position
        b = self.member_length - self.position
        length = self.member_length
        node_1_releases = self.node_1_releases
        node_2_releases = self.node_2_releases
        merge_releases = np.array(node_1_releases + node_2_releases)
        # Totally fixed-end  actions
        moment_left_y = self.components[2]*a*b**2/length**2
        moment_right_y = -self.components[2]*a**2*b/length**2
        force_left_z = -self.components[2]*b**2*(3*a + b)/length**3
        force_right_z = -self.components[2]*a**2*(3*b + a)/length**3
        moment_left_z = -self.components[1]*a*b**2/length**2
        moment_right_z = self.components[1]*a**2*b/length**2
        force_left_y = -self.components[1]*b**2*(3*a + b)/length**3
        force_right_y = -self.components[1]*a**2*(3*b + a)/length**3
        force_left_x = -self.components[0]*b/length
        force_right_x = -self.components[0]*a/length
        moment_left_x = 0
        moment_right_x = 0
        # Releasing the totally fixed structure
        action_array = np.array([force_left_x, force_left_y, force_left_z, \
                moment_left_x, moment_left_y, moment_left_z, force_right_x, \
                force_right_y, force_right_z, moment_right_x, moment_right_y, \
                moment_right_z])
        actions_gone_due_to_releases = action_array[merge_releases]
        actions_stayed = action_array[~merge_releases]
        displacements_due_to_releases = -actions_gone_due_to_releases/\
                self.initial_stiffness[merge_releases,merge_releases]
        stiffness_stayed_actions = self.initial_stiffness[:,merge_releases]\
                [~merge_releases,:]
        new_actions_due_to_releases = stiffness_stayed_actions @\
                displacements_due_to_releases
        summed_actions = actions_stayed + new_actions_due_to_releases
        action_array[~merge_releases] = summed_actions
        action_array = action_array * ~merge_releases
        return Force(-action_array[:3]), Moment(-action_array[3:6]), \
                Force(-action_array[6:9]), Moment(-action_array[9:12])


class Moment(ActionPuntual):
    def __init__(self, compoenents: Tuple[float, float, float]):
        super().__init__(compoenents)

    def __add__(self, other):
        if isinstance(other, Moment):
            return Moment((self.components + other.components).tolist())
        else:
            raise TypeError('You cannot add differents type of Actions')

    def compute_equivalent_joint_loads(self):
        """
        Equivalent Joint Loads for Forces 
        """
        # Reassingning variables (easy to handle)
        a = self.position
        b = self.member_length - self.position
        length = self.member_length
        node_1_releases = self.node_1_releases
        node_2_releases = self.node_2_releases
        merge_releases = np.array(node_1_releases + node_2_releases)
        # Totally fixed-end  actions
        force_left_z = 6*self.components[1]*a*b/length**3
        force_right_z = -6*self.components[1]*a*b/length**3
        moment_left_y = self.components[1]*b*(b - 2*a)/length**2
        moment_right_y = self.components[1]*a*(a - 2*b)/length**2
        force_left_y = 6*self.components[2]*a*b/length**3
        force_right_y = -6*self.components[2]*a*b/length**3
        moment_left_z = self.components[2]*b*(b - 2*a)/length**2
        moment_right_z = self.components[2]*a*(a - 2*b)/length**2
        force_left_x = 0
        force_right_x = 0
        moment_left_x = -self.components[0]*b/length
        moment_right_x = -self.components[0]*a/length
        # Releasing the totally fixed structure
        action_array = np.array([force_left_x, force_left_y, force_left_z,
            moment_left_x, moment_left_y, moment_left_z, force_right_x, 
            force_right_y, force_right_z, moment_right_x, moment_right_y, 
            moment_right_z])
        actions_gone_due_to_releases = action_array[merge_releases]
        actions_stayed = action_array[~merge_releases]
        displacements_due_to_releases = -actions_gone_due_to_releases/\
                self.initial_stiffness[merge_releases,merge_releases]
        stiffness_stayed_actions = self.initial_stiffness[:,merge_releases]\
                [~merge_releases,:]
        new_actions_due_to_releases = stiffness_stayed_actions @\
                displacements_due_to_releases
        summed_actions = actions_stayed + new_actions_due_to_releases
        action_array[~merge_releases] = summed_actions
        action_array = action_array * ~merge_releases
        return Force(-action_array[:3]), Moment(action_array[3:6]), \
                Force(-action_array[6:9]), Moment(action_array[9:12])
