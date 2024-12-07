"""Linear Entity classes."""


from __future__ import annotations

from typing import TYPE_CHECKING

from .abc import (ALinearEntity,
                  AConcreteLinearEntity,
                  ALinearEntityAtInf,

                  ALine,

                  AConcreteLine,
                  AConcreteDirectedLine,

                  ALineAtInf,
                  ADirectedLineAtInf)

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import LiteralString


__all__: Sequence[LiteralString] = ('ALinearEntity',
                                    'AConcreteLinearEntity',
                                    'ALinearEntityAtInf',

                                    'ALine',

                                    'AConcreteLine',
                                    'AConcreteDirectedLine',

                                    'ALineAtInf',
                                    'ADirectedLineAtInf')
