from __future__ import annotations


__all__ = 'Session', 'DEFAULT_SESSION'


from sympy.assumptions.assume import AssumptionsContext

from ..._util._tmp import TMP_NAME_FACTORY
from ..._util._type import OptionalStrOrCallableReturningStrType
from ._entity import _EntityABC


class Session:
    def __init__(self, name: OptionalStrOrCallableReturningStrType = TMP_NAME_FACTORY, /) -> None:
        if callable(name):
            name = name()
        elif not name:
            name = TMP_NAME_FACTORY()
        _EntityABC._validate_name(name)
        self.name = name

        self.entities = {}

        self.sympy_assumptions = AssumptionsContext()

    def __repr__(self) -> str:
        return f"Geometry Session{f' {name.upper()}' if (name := self.name) else ''}"

    __str__ = __repr__

    def __setattr__(self, name: str, value, /) -> None:
        if isinstance(value, _EntityABC):
            value.session = self
            self.entities[name] = value

        else:
            object.__setattr__(self, name, value)

    def __setitem__(self, name: str, entity: _EntityABC, /) -> None:
        _EntityABC._validate_name(name)

        assert isinstance(entity, _EntityABC), \
            TypeError(f'*** {entity} NOT OF TYPE {_EntityABC.__name__} ***')

        entity.session = self
        self.entities[name] = entity

    def __getattr__(self, name: str, /) -> _EntityABC:
        return self.entities[name]

    def __getitem__(self, name: str, /) -> _EntityABC:
        _EntityABC._validate_name(name)

        return self.entities[name]

    def __delattr__(self, name: str) -> None:
        del self.entities[name]

    def __delitem__(self, name: str) -> None:
        _EntityABC._validate_name(name)

        del self.entities[name]


# Global Geometry Session
DEFAULT_SESSION = Session('')
