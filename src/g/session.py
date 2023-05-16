"""Session."""


from collections.abc import Callable, Sequence
from typing import Any, LiteralString, Optional, Self

from sympy.assumptions.assume import AssumptionsContext

from ._alg import _AlgBackendABC, SymPyBackend
from ._art import _ArtFrontendABC, MAnimFrontend
from ._geom.entity.abstract import _EntityABC
from ._util.unique_name import UNIQUE_NAME_FACTORY


__all__: Sequence[LiteralString] = 'Session', 'DEFAULT_SESSION'


class Session:
    """Session."""

    def __init__(self: Self, name: Optional[str] = None, /, *,
                 alg_backend: _AlgBackendABC = SymPyBackend(),
                 art_frontend: _ArtFrontendABC = MAnimFrontend()) -> None:
        """Initialize session."""
        # assign name
        self.name: str = UNIQUE_NAME_FACTORY() if name is None else name

        # assign algebra backend & art frontend
        self.alg_backend: _AlgBackendABC = alg_backend
        self.art_frontend: _ArtFrontendABC = art_frontend

        # initialize entities collection
        self.entities: dict[str, _EntityABC] = dict[str, _EntityABC]()

        # initialize SymPy assumptions
        self.sympy_assumptions: AssumptionsContext = AssumptionsContext()

    def __repr__(self: Self, /) -> str:
        """Return string representation."""
        return f"Geometry Session{f' {_.upper()}' if (_ := self.name) else ''}"

    __str__: Callable[[Self], str] = __repr__

    def __setattr__(self: Self, name: str, value: Any, /) -> None:
        """Assign entity, if applicable."""
        if isinstance(value, _EntityABC):
            # validate entity name
            _EntityABC._validate_name(name)

            # assign entity session
            value.session: Self = self

            # add entity to session's entities collection
            self.entities[name]: _EntityABC = value

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
