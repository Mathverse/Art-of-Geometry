"""Session."""


from collections.abc import Sequence
from typing import Any, Self

from sympy.assumptions.assume import AssumptionsContext

from .._util.type import OptionalStrOrCallableReturningStr
from .._util.unique_name import UNIQUE_NAME_FACTORY
from .entity import _EntityABC


__all__: Sequence[str] = 'Session', 'DEFAULT_SESSION'


class Session:
    """Session."""

    def __init__(self: Self,
                 name: OptionalStrOrCallableReturningStr = UNIQUE_NAME_FACTORY, /) -> None:  # noqa: E501
        """Initialize session."""
        # generate name if not already given as string
        if callable(name):
            name: str = name()
        elif not name:
            name: str = UNIQUE_NAME_FACTORY()

        # validate name
        _EntityABC._validate_name(name)

        # assign name
        self.name: str = name

        # initialize entities collection
        self.entities: dict[str, _EntityABC] = dict[str, _EntityABC]()

        # initialize SymPy assumptions
        self.sympy_assumptions: AssumptionsContext = AssumptionsContext()

    def __repr__(self: Self, /) -> str:
        """Return string representation."""
        return f"Geometry Session{f' {_.upper()}' if (_ := self.name) else ''}"

    __str__ = __repr__

    def __setattr__(self: Self, name: str, value: Any, /) -> None:
        """Assign entity, if applicable."""
        if isinstance(value, _EntityABC):
            # validate entity name
            _EntityABC._validate_name(name)

            # assign entity session
            value.session: Self = self

            # add entity to session's entities collection
            self.entities[name]: Any = value

        else:
            object.__setattr__(self, name, value)

    def __setitem__(self: Self, name: str, entity: _EntityABC, /) -> None:
        """Assign entity."""
        # validate entity name
        _EntityABC._validate_name(name)

        # validate entity type
        assert isinstance(entity, _EntityABC), \
            TypeError(f'*** {entity} NOT OF TYPE {_EntityABC.__name__} ***')

        # assign entity session
        entity.session: Self = self

        # add entity to session's entities collection
        self.entities[name]: _EntityABC = entity

    def __getattr__(self: Self, name: str, /) -> _EntityABC:
        """Get entity by name."""
        return self.entities[name]

    def __getitem__(self: Self, name: str, /) -> _EntityABC:
        """Get entity by name."""
        # validate entity name
        _EntityABC._validate_name(name)

        return self.entities[name]

    def __delattr__(self: Self, name: str, /) -> None:
        """Delete entity by name."""
        del self.entities[name]

    def __delitem__(self: Self, name: str, /) -> None:
        """Delete entity by name."""
        # validate entity name
        _EntityABC._validate_name(name)

        del self.entities[name]


# default/global session
DEFAULT_SESSION: Session = Session('')
