__all_ = 'ConicInR2', 'ConicR2', 'Conic'


from .. import _EuclidR2GeometryEntityABC


class ConicInR2(_EuclidR2GeometryEntityABC):
    def __init__(self):
        pass


# aliases
Conic = ConicR2 = ConicInR2
