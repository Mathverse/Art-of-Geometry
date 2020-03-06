__all__ = 'EuclideanR2Space', 'EuclideanR2HalfSpace'


from .._abc._space import _EuclideanSpaceABC, _EuclideanHalfSpaceABC


class EuclideanR2Space(_EuclideanSpaceABC):
    pass


class EuclideanR2HalfSpace(_EuclideanHalfSpaceABC):
    pass
