from stiffpy.member import Member
from matplotlib import pyplot as plt


class PlotterMember:
    def __init__(self, member: Member):
        # initalize attributes
        self.member: Member = member

    def draw(self, axs: plt.Axes):
        """
        Method to draw the member in the axes

        Note
        ----
        Because a member drown in the axes is just a line, is recommended to use
        this method as a helper for other methods
        """
        # Draw Member
        axs.plot(
                [self.member.node_1.r[0], self.member.node_2.r[0]],
                [self.member.node_1.r[1], self.member.node_2.r[1]],
                color="black")

    # Internal Actions
    def draw_axial(self, axs: plt.Axes):
        """
        Method to draw Axial Force Diagram of a member
        """
        axs.plot(self.member.domain, self.member.axial_force)
        axs.set_title('Axial Force Diagram')
        axs.set_ylabel('Axial Force')
        axs.set_xlabel('Position')
        axs.grid()

    def draw_torsion(self, axs: plt.Axes):
        """
        Method to draw Torsion Diagram of a member
        """
        axs.plot(self.member.domain, self.member.torsion)
        axs.set_title('Torsion Diagram')
        axs.set_ylabel('Torsion')
        axs.set_xlabel('Position')
        axs.grid()

    def draw_shear_xy(self, axs: plt.Axes):
        """
        Method to draw shear diagrams in the local Y and Z axis
        Note
        ----
        The notation XY means that the shear force is in the XY plane
        """
        shear_xy, _ = self.member.shear
        # Plot XY Shear
        axs.plot(self.member.domain, shear_xy)
        axs.set_title('Shear Diagram XY')
        axs.set_ylabel('Shear XY')
        axs.set_xlabel('Position')
        axs.grid()

    def draw_shear_xz(self, axs: plt.Axes):
        """
        Method to draw shear diagrams in the local Y and Z axis
        Note
        ----
        The notation XZ means that the shear force is in the XZ plane
        """
        _, shear_xz = self.member.shear
        # Plot XZ Shear
        axs.plot(self.member.domain, shear_xz)
        axs.set_title('Shear Diagram XZ')
        axs.set_ylabel('Shear XZ')
        axs.set_xlabel('Position')
        axs.grid()

    def draw_bending_xy(self, axs: plt.Axes, reverse: bool=False):
        """
        Method to draw bending moment diagrams in the local Y and Z axis
        Note
        ----
        # Check The notation XY means that the beding moment is in the XY plane
        """
        bending_xy, _ = self.member.bending
        # Plot XY Bending Moment
        axs.plot(self.member.domain, bending_xy)
        axs.set_title("Bending Diagram XY")
        axs.set_ylabel("Bending XY")
        axs.set_xlabel("Position")
        axs.grid()
        # Reverse Y Axis
        if not reverse:
            axs.invert_yaxis()

    def draw_bending_xz(self, axs: plt.Axes, reverse: bool=False):
        """
        Method to draw bending moment diagrams in the local Y and Z axis
        Note
        ----
        # Check The notation XZ means that the bending moment is perpendicular to the XZ plane
        """
        _, bending_xz = self.member.bending
        # Plot XZ Bending Moment
        axs.plot(self.member.domain, bending_xz)
        axs.set_title("Bending Diagram XZ")
        axs.set_ylabel("Bending XZ")
        axs.set_xlabel("Position")
        axs.grid()
        # Reverse Z Axis
        if not reverse:
            axs.invert_yaxis()

    # Deformations
    def draw_deflection_xy(self, axs: plt.Axes):
        """
        Method to draw deflection
        Note
        ----
        The notation XY indicates ...........
        """
        deflection_xy, _ = self.member.deflection
        # Plot XY deflection
        axs.plot(self.member.domain, deflection_xy)
        axs.set_title("Deflection XY")
        axs.set_ylabel('Deflection XY')
        axs.set_xlabel("Position")
        axs.grid()

    def draw_deflection_xz(self, axs: plt.Axes):
        """
        Method to draw deflection
        Note
        ----
        The notation XZ indicates ...........
        """
        _, deflection_xz = self.member.deflection
        # Plot XZ deflection
        axs.plot(self.member.domain, deflection_xz)
        axs.set_title("Deflection XZ")
        axs.set_ylabel("Deflection XZ")
        axs.set_xlabel("Position")
        axs.grid()

    def draw_axial_deformation(self, axs: plt.Axes):
        """
        Method to draw axial deflection
        """
        axial_def = self.member.axial_deformation
        # Plot Axial Deformation
        axs.plot(self.member.domain, axial_def)
        axs.set_title("Axial Deformation")
        axs.set_ylabel("Deformation")
        axs.set_xlabel("Position")
        axs.grid()
