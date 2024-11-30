__all__ = 'EuclideanR1Space', 'EuclideanR1HalfSpace'


from .._core._space import _EuclideanSpaceABC, _EuclideanHalfSpaceABC


class EuclideanR1Space(_EuclideanSpaceABC):
    pass


class EuclideanR1HalfSpace(_EuclideanHalfSpaceABC):
    pass
