"""Abstract Geometry Entity."""


from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from functools import cached_property
from typing import LiteralString, Self, TYPE_CHECKING

from sympy.core.expr import Expr
from sympy.geometry.entity import GeometryEntity

from .abc import _EntityABC
from .decor import assign_entity_dependencies_and_name

if TYPE_CHECKING:
    from ..linear import _LinearEntityABC, _LineABC
    from ..point import _PointABC
    from ..vector import _VectorABC


__all__: Sequence[LiteralString] = ('_GeomEntityABC',)


@assign_entity_dependencies_and_name
class _GeomEntityABC(_EntityABC, GeometryEntity):
    """Abstract Geometry Entity."""

    @property
    def name(self: Self, /) -> str:
        """Get name."""
        return getattr(self, self._NAME_ATTR_KEY)

    @name.setter
    def name(self: Self, name: str, /) -> None:
        """Assign name."""
        # validate name
        self._validate_name(name)

        # assign name if different
        if name != getattr(self, self._NAME_ATTR_KEY):
            setattr(self, self._NAME_ATTR_KEY, name)

    @name.deleter
    def name(self: Self, /) -> None:
        """Delete name / reset it to None."""
        setattr(self, self._NAME_ATTR_KEY, None)

    @abstractmethod
    def copy(self: Self, /) -> _GeomEntityABC:
        """Copy."""
        raise NotImplementedError

    # alias
    def same(self: Self, /) -> _GeomEntityABC:
        """Copy."""
        raise self.copy()

    # EQUATION & PARAMETRIC EQUATIONS
    @cached_property
    @abstractmethod
    def equation(self: Self, /) -> Expr:
        """Cartesian equation."""
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def parametric_equations(self: Self, /) -> tuple[Expr, ...]:
        """Parametric equations."""
        raise NotImplementedError

    # INCIDENCE
    @abstractmethod
    def incident_with(self: Self, other_geometry_entity: _GeomEntityABC, /) -> bool:  # noqa: E501
        """Check incidence."""
        raise NotImplementedError

    # NORMAL DIRECTION
    @abstractmethod
    def normal_direction_at_point(self: Self, point: _PointABC, /) -> _VectorABC:  # noqa: E501
        raise NotImplementedError

    # alias
    def normal_direction(self: Self, point: _PointABC, /) -> _VectorABC:
        return self.normal_direction_at_point(point)

    def normal(self: Self, point: _PointABC, /) -> _VectorABC:
        return self.normal_direction_at_point(point)

    # PERPENDICULAR LINE
    @abstractmethod
    def perpendicular_line_at_point(self: Self, point: _PointABC, /) -> _LineABC:  # noqa: E501
        raise NotImplementedError

    # alias
    def perpendicular_line(self: Self, point: _PointABC, /) -> _LineABC:
        raise self.perpendicular_line_at_point(point)

    # TANGENT
    @abstractmethod
    def tangent_at_point(self: Self, point: _PointABC, /) -> _LinearEntityABC:
        raise NotImplementedError

    # alias
    def tangent(self: Self, point: _PointABC, /) -> _LinearEntityABC:
        return self.tangent_at_point(point)

    # CUTTING / INTERSECTION
    @abstractmethod
    def cut(self: Self, other_geometry_entity: _GeomEntityABC, /) \
            -> (_GeomEntityABC | set[_GeomEntityABC]):
        """Intersection."""
        raise NotImplementedError

    # aliases
    def intersect(self: Self, other_geometry_entity: _GeomEntityABC, /) \
            -> (_GeomEntityABC | set[_GeomEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)

    def intersection(
            self: Self, other_geometry_entity: _GeomEntityABC, /) \
            -> (_GeomEntityABC | set[_GeomEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)

    def __and__(self: Self, other_geometry_entity: _GeomEntityABC, /) \
            -> (_GeomEntityABC | set[_GeomEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)

    def __rand__(self: Self, other_geometry_entity: _GeomEntityABC, /) \
            -> (_GeomEntityABC | set[_GeomEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)
