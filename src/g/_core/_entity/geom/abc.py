"""Abstract Geometric Entity.

Geometric Entities are entities that can be concretized/materialized/
physicalized/realized/visualized into tangible/visible shapes.
"""


from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from ..abc import AnEntity

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString, Self

    from ..point import APoint
    from ..space import ALinearEntity, ALine
    from ..vector import Vector


__all__: Sequence[LiteralString] = ('AGeomEntity',)


class AGeomEntity(AnEntity):
    """Abstract Geometric Entity."""

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
    def pick_a_point(self, *args, **kwargs) -> APoint:
        """Pick a Point on this Geometric Entity."""
        raise NotImplementedError

    @abstractmethod
    def copy(self: Self, /) -> Self:
        """Copy."""
        raise NotImplementedError

    # alias
    def same(self: Self, /) -> Self:
        """Copy."""
        raise self.copy()

    # INCIDENCE
    @abstractmethod
    def incident_with(self: Self, other_geom_entity: AGeomEntity, /) -> bool:
        """Check incidence."""
        raise NotImplementedError

    # NORMAL DIRECTION
    @abstractmethod
    def normal_direction_at_point(self: Self, point: APoint, /) -> Vector:
        raise NotImplementedError

    # alias
    def normal_direction(self: Self, point: APoint, /) -> Vector:
        return self.normal_direction_at_point(point)

    def normal(self: Self, point: APoint, /) -> Vector:
        return self.normal_direction_at_point(point)

    # PERPENDICULAR LINE
    @abstractmethod
    def perpendicular_line_at_point(self: Self, point: APoint, /) -> ALine:
        raise NotImplementedError

    # alias
    def perpendicular_line(self: Self, point: APoint, /) -> ALine:
        raise self.perpendicular_line_at_point(point)

    # TANGENT
    @abstractmethod
    def tangent_at_point(self: Self, point: APoint, /) -> ALinearEntity:
        raise NotImplementedError

    # alias
    def tangent(self: Self, point: APoint, /) -> ALinearEntity:
        return self.tangent_at_point(point)

    # CUTTING / INTERSECTION
    @abstractmethod
    def cut(self: Self, other_geom_entity: AGeomEntity, /) \
            -> (AGeomEntity | set[AGeomEntity]):
        """Intersection."""
        raise NotImplementedError

    # aliases
    def intersect(self: Self, other_geom_entity: AGeomEntity, /) \
            -> (AGeomEntity | set[AGeomEntity]):
        """Intersection."""
        return self.cut(other_geom_entity)

    def intersection(self: Self, other_geom_entity: AGeomEntity, /) \
            -> (AGeomEntity | set[AGeomEntity]):
        """Intersection."""
        return self.cut(other_geom_entity)

    def __and__(self: Self, other_geom_entity: AGeomEntity, /) \
            -> (AGeomEntity | set[AGeomEntity]):
        """Intersection."""
        return self.cut(other_geom_entity)

    def __rand__(self: Self, other_geom_entity: AGeomEntity, /) \
            -> (AGeomEntity | set[AGeomEntity]):
        """Intersection."""
        return self.cut(other_geom_entity)
