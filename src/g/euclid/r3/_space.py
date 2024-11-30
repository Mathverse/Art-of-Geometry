__all__ = 'EuclideanR3Space', 'EuclideanR3HalfSpace'


from ..core._space import _EuclideanSpaceABC, _EuclideanHalfSpaceABC


class EuclideanR3Space(_EuclideanSpaceABC):
    pass


class EuclideanR3HalfSpace(_EuclideanHalfSpaceABC):
    pass
