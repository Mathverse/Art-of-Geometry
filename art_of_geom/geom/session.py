from __future__ import annotations   # to avoid circular import b/w _EntityABC & Session


__all__ = 'Session', 'DEFAULT_SESSION'


from sympy.assumptions.assume import AssumptionsContext
from typing import TYPE_CHECKING
from uuid import uuid4

from ..util.types import OptionalStrType


if TYPE_CHECKING:   # to avoid circular import b/w _EntityABC & Session
    from .abc import _EntityABC


class Session:
    def __init__(self, name: OptionalStrType = None, /) -> None:
        self.name = \
            name \
            if isinstance(name, str) \
            else str(uuid4())

        self.entities = {}

        self.sympy_assumptions = AssumptionsContext()

    def __repr__(self) -> str:
        return f"Geometry Session{f' {name.upper()}' if (name := self.name) else ''}"

    __str__ = __repr__

    @property
    def _str_prefix(self) -> str:
        return f'{name}: ' \
            if (name := self.name) \
          else ''

    def __setattr__(self, name: str, value, /) -> None:
        from .abc import _EntityABC

        if isinstance(value, _EntityABC):
            value.session = self
            self.entities[name] = value

        else:
            object.__setattr__(self, name, value)

    def __setitem__(self, name: str, entity: _EntityABC, /) -> None:
        from .abc import _EntityABC

        _EntityABC._validate_name(name)

        assert isinstance(entity, _EntityABC), \
            TypeError(f'*** {entity} NOT OF TYPE {_EntityABC.__name__} ***')

        entity.session = self
        self.entities[name] = entity

    def __getattr__(self, name: str, /) -> _EntityABC:
        return self.entities[name]

    def __getitem__(self, name: str, /) -> _EntityABC:
        from .abc import _EntityABC

        _EntityABC._validate_name(name)

        return self.entities[name]

    def __delattr__(self, name: str) -> None:
        del self.entities[name]

    def __delitem__(self, name: str) -> None:
        from .abc import _EntityABC

        _EntityABC._validate_name(name)

        del self.entities[name]


# Global Geometry Session
DEFAULT_SESSION = Session('')
