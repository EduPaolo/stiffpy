from ..structure import Structure


class Spring(Structure):
    def draw_deformations(self, factor=1):
        super().draw_deformations('2d', factor)
