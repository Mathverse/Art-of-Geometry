__all__ = 'CircleInR2_HyperboloidInR2I',


from ..r2.circle import CircleInR2
from .abc import _SurfaceInR2IABC
from .coord import X, Y, Z


class CircleInR2_HyperboloidInR2I(_SurfaceInR2IABC):
    def __init__(self, circle_in_r2: CircleInR2):
        assert isinstance(circle_in_r2, CircleInR2), \
            TypeError(
                '*** {} NOT {} ***'
                .format(circle_in_r2, CircleInR2.__name__))

        self.circle_in_r2 = circle_in_r2

    @property
    def equation(self):
        return (X - self.circle_in_r2.center.x) ** 2 \
             + (Y - self.circle_in_r2.center.y) ** 2 \
             - Z ** 2 \
             - self.circle_in_r2.radius ** 2
