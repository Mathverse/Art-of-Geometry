__all__ = 'Session', 'GLOBAL_SESSION'


from sympy.assumptions.assume import AssumptionsContext
from typing import Optional
from uuid import uuid4

from .abc import _GeometryEntityABC


class Session:
    def __init__(self, name: Optional[str] = None, /) -> None:
        self.name = \
            name \
            if isinstance(name, str) and name \
            else str(uuid4())

        self.geometry_entities = {}

        self.sympy_assumptions = AssumptionsContext()

    def __repr__(self) -> str:
        return f'Geometry Session "{self.name}"'

    __str__ = __repr__

    @staticmethod
    def _validate_geometry_entity_name(name: str, /) -> None:
        assert isinstance(name, str) and name, \
            TypeError(f'*** {name} NOT NON-EMPTY STRING ***')

    def __setattr__(self, name: str, value, /) -> None:
        if isinstance(value, _GeometryEntityABC):
            value.session = self
            self.geometry_entities[name] = value

        else:
            object.__setattr__(self, name, value)

    def __setitem__(self, name: str, geometry_entity: _GeometryEntityABC, /) -> None:
        self._validate_geometry_entity_name(name)

        assert isinstance(geometry_entity, _GeometryEntityABC), \
            TypeError(f'*** {geometry_entity} NOT OF TYPE {_GeometryEntityABC.__name__} ***')

        geometry_entity.session = self
        self.geometry_entities[name] = geometry_entity

    def __getattr__(self, name: str, /) -> _GeometryEntityABC:
        return self.geometry_entities[name]

    def __getitem__(self, name: str, /) -> _GeometryEntityABC:
        self._validate_geometry_entity_name(name)

        return self.geometry_entities[name]

    def __delattr__(self, name: str) -> None:
        del self.geometry_entities[name]

    def __delitem__(self, name: str) -> None:
        self._validate_geometry_entity_name(name)

        del self.geometry_entities[name]


# Global Geometry Session
GLOBAL_SESSION = Session('GLOBAL GEOMETRY SESSION')