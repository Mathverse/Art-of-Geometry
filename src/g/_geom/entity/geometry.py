"""Abstract Entity."""


from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable, Sequence
from functools import cached_property, wraps
from inspect import (getmembers,
                     isabstract, isclass, isfunction, ismethoddescriptor,
                     Parameter, signature)
from pprint import pprint
import sys
from typing import Any, LiteralString, Optional, Self, TYPE_CHECKING

from sympy.core.expr import Expr
from sympy.core.symbol import Symbol
from sympy.geometry.entity import GeometryEntity

from .._util import debug
from .._util.inspect import is_static_method, is_class_method, is_instance_method, describe  # noqa: E501
from .._util.type import CallableReturningStr, OptionalStrOrCallableReturningStr  # noqa: E501
from .._util.unique_name import UNIQUE_NAME_FACTORY

if TYPE_CHECKING:  # avoid circular import between _EntityABC & Session
    from .session import Session
    from .point import _PointABC
    from .line import _LinearEntityABC, _LineABC



__all__: Sequence[LiteralString] = ('_GeometryEntityABC',)


@_EntityABC.assign_name_and_dependencies
class _GeometryEntityABC(_EntityABC, GeometryEntity):
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
    def copy(self: Self, /) -> _GeometryEntityABC:
        """Copy."""
        raise NotImplementedError

    # alias
    def same(self: Self, /) -> _GeometryEntityABC:
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
    def incident_with(self: Self, other_geometry_entity: _GeometryEntityABC, /) -> bool:  # noqa: E501
        """Check incidence."""
        raise NotImplementedError

    # NORMAL DIRECTION
    @abstractmethod
    def normal_direction_at_point(self: Self, point: _PointABC, /) -> _PointABC:  # noqa: E501
        raise NotImplementedError

    # alias
    def normal_direction(self: Self, point: _PointABC, /) -> _PointABC:
        return self.normal_direction_at_point(point)

    def normal(self: Self, point: _PointABC, /) -> _PointABC:
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
    def cut(self: Self, other_geometry_entity: _GeometryEntityABC, /) \
            -> (_GeometryEntityABC | set[_GeometryEntityABC]):
        """Intersection."""
        raise NotImplementedError

    # aliases
    def intersect(self: Self, other_geometry_entity: _GeometryEntityABC, /) \
            -> (_GeometryEntityABC | set[_GeometryEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)

    def intersection(
            self: Self, other_geometry_entity: _GeometryEntityABC, /) \
            -> (_GeometryEntityABC | set[_GeometryEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)

    def __and__(self: Self, other_geometry_entity: _GeometryEntityABC, /) \
            -> (_GeometryEntityABC | set[_GeometryEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)

    def __rand__(self: Self, other_geometry_entity: _GeometryEntityABC, /) \
            -> (_GeometryEntityABC | set[_GeometryEntityABC]):
        """Intersection."""
        return self.cut(other_geometry_entity)
