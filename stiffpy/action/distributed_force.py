from typing import Tuple
import numpy as np
from .action_distributed import ActionDistributed
from .actions import Force, Moment


class DistributedForce(ActionDistributed):
    def __init__(self,
            initial_magnitudes: Tuple[float, float, float],
            final_magnitudes: Tuple[float, float, float],
            length: float):
        super().__init__(initial_magnitudes, final_magnitudes, length)
    
    def compute_equivalent_joint_loads(self):
        """
        Equivalent Joint Loads for Distributed Forces
        """
        # Reassingning variables (easy to handle)
        a = self.position
        c = self.length
        b = self.member_length - a - c
        length = self.member_length
        node_1_releases = self.node_1_releases
        node_2_releases = self.node_2_releases
        merge_releases = np.array(node_1_releases + node_2_releases)
        harmonic = 1 + b/(length - a) + b**2/(length - a)**2
        # Totally fixed-end  actions
        # Forces X-Y, Moments Z
        initial = self.initial_magnitudes[1]
        final = self.final_magnitudes[1]
        ra_1 = initial*(length - a)**3/20/length**3
        ra_2 = final*(length - a)**3/20/length**3
        force_left_y =  -(ra_1*(7*length + 8*a - b*(3*length + 2*a)/\
                (length - a)*harmonic + 2*b**4/(length - a)**3) + \
                ra_2*((3*length + 2*a)*harmonic - b**3/(length - a)**2*\
                (2 + (15*length - 8*b)/(length - a))))
        moment_left_z = -c*(30*a*b**2*initial + 30*a*b**2*final + 
                40*a*b*c*initial + 20*a*b*c*final + 15*a*c**2*initial + 
                5*a*c**2*final + 10*b**2*c*initial + 20*b**2*c*final + 
                10*b*c**2*initial + 10*b*c**2*final + 3*c**3*initial + 
                2*c**3*final)/(60*(a**2 + 2*a*b + 2*a*c + b**2 + 2*b*c + c**2))
        force_right_y = -((final + initial)/2*(length - a - b) + force_left_y)
        moment_right_z = c*(30*a**2*b*initial + 30*a**2*b*final + 
                20*a**2*c*initial + 10*a**2*c*final + 20*a*b*c*initial + 
                40*a*b*c*final + 10*a*c**2*initial + 10*a*c**2*final + 
                5*b*c**2*initial + 15*b*c**2*final + 2*c**3*initial + 
                3*c**3*final)/(60*(a**2 + 2*a*b + 2*a*c + b**2 + 2*b*c + c**2))        
        # Forces X-Z, Moments Y
        initial = self.initial_magnitudes[2]
        final = self.final_magnitudes[2]
        ra_1 = initial*(length - a)**3/20/length**3
        ra_2 = final*(length - a)**3/20/length**3
        force_left_z = -(ra_1*(7*length + 8*a - b*(3*length + 2*a)/\
                (length - a)*harmonic + 2*b**4/(length - a)**3) + 
                ra_2*((3*length + 2*a)*harmonic - b**3/(length - a)**2*
                    (2 + (15*length - 8*b)/(length - a))))
        moment_left_y = c*(30*a*b**2*initial + 30*a*b**2*final + 
                40*a*b*c*initial + 20*a*b*c*final + 15*a*c**2*initial + 
                5*a*c**2*final + 10*b**2*c*initial + 20*b**2*c*final + 
                10*b*c**2*initial + 10*b*c**2*final + 3*c**3*initial + 
                2*c**3*final)/(60*(a**2 + 2*a*b + 2*a*c + b**2 + 2*b*c + c**2))
        force_right_z = -((final + initial)/2*(length - a - b) + force_left_z)
        moment_right_y = -c*(30*a**2*b*initial + 30*a**2*b*final + 
                20*a**2*c*initial + 10*a**2*c*final + 20*a*b*c*initial + 
                40*a*b*c*final + 10*a*c**2*initial + 10*a*c**2*final + 
                5*b*c**2*initial + 15*b*c**2*final + 2*c**3*initial + 
                3*c**3*final)/(60*(a**2 + 2*a*b + 2*a*c + b**2 + 2*b*c + c**2))
        # Forces X, Moments X
        force_left_x = -self.final_magnitudes[0]*c*(length - a + b)/2/length
        force_right_x = -self.final_magnitudes[0]*c*(length + a - b)/2/length
        moment_left_x = 0
        moment_right_x = 0
        # Releasing the totally fixed structure (Routine)
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
        return Force(-action_array[:3]), Moment(-action_array[3:6]), \
                Force(-action_array[6:9]), Moment(-action_array[9:12])
