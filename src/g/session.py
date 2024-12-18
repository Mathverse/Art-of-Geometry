"""Session."""


from __future__ import annotations

from typing import TYPE_CHECKING

from sympy.assumptions.assume import AssumptionsContext

from ._core import AnEntity

from ._alg.abc import _AlgBackendABC
from ._alg.sympy import SymPyBackend

from ._art.abc import _ArtFrontendABC
from ._art.manim import MAnimFrontend

from ._util.type import OptionalStr
from ._util.unique_name import UNIQUE_NAME_FACTORY

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
    from typing import Any, LiteralString, Self

    from ._core import ASpace


__all__: Sequence[LiteralString] = 'Session', 'DEFAULT_SESSION'


class Session:
    """Session."""

    def __init__(self: Self, name: OptionalStr = None, /, *,
                 ambient_space: ASpace = None,
                 alg_backend: _AlgBackendABC = SymPyBackend(),
                 art_frontend: _ArtFrontendABC = MAnimFrontend()) -> None:
        """Initialize session."""
        # assign name
        self.name: str = UNIQUE_NAME_FACTORY() if name is None else name

        # assign ambient space
        self.ambient_space: ASpace = ambient_space

        # assign algebra backend & art frontend
        self.alg_backend: _AlgBackendABC = alg_backend
        self.art_frontend: _ArtFrontendABC = art_frontend

        # initialize entities collection
        self.entities: dict[str, AnEntity] = dict[str, AnEntity]()

        # initialize SymPy assumptions
        self.sympy_assumptions: AssumptionsContext = AssumptionsContext()

    def __repr__(self: Self, /) -> str:
        """Return string representation."""
        return f"Geometry Session{f' {_.upper()}' if (_ := self.name) else ''}"

    __str__: Callable[[Self], str] = __repr__

    def _assign_entity(self: Self, name: str, entity: AnEntity, /,
                       *, validate_type: bool = True) -> None:
        """Assign entity."""
        # validate entity name
        AnEntity._validate_name(name)

        # validate entity type
        if validate_type:
            assert isinstance(entity, AnEntity), \
                TypeError(f'*** {entity} NOT OF TYPE {AnEntity.__name__} ***')  # noqa: E501

        # assign entity session
        entity.session: Self = self

        # add entity to session's entities collection
        self.entities[name]: AnEntity = entity

    def __setattr__(self: Self, name: str, value: Any, /) -> None:
        """Assign entity, if applicable."""
        if isinstance(value, AnEntity):
            self._assign_entity(name, value, validate_type=False)

        else:
            object.__setattr__(self, name, value)

    def __setitem__(self: Self, name: str, entity: AnEntity, /) -> None:
        """Assign entity."""
        self._assign_entity(name, entity)

    def __getattr__(self: Self, name: str, /) -> AnEntity:
        """Get entity by name."""
        return self.entities[name]

    def __getitem__(self: Self, name: str, /) -> AnEntity:
        """Get entity by name."""
        return self.entities[name]

    def __delattr__(self: Self, name: str, /) -> None:
        """Delete entity by name."""
        del self.entities[name]

    def __delitem__(self: Self, name: str, /) -> None:
        """Delete entity by name."""
        del self.entities[name]


# default/global session
DEFAULT_SESSION: Session = Session('')
