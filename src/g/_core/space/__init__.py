"""Abstract Space base classes.

In this Art of Geometry package, Spaces are set-like geometric entities
containing Points and in/on which Points can be moved/transformed.

This Art of Geometry package primarily deals with SMOOTHLY CONTINUOUS Spaces,
in/on which Points' movements/transformations are characterized by smoothly/
differentiably continuous functions and/or coordinate/parametric equations.

The 3-dimensional Euclidean space, 2-dimensional Euclidean flat planes,
2-dimensional spherical/elliptical/hyperbolical surfaces, 1-dimensional
Euclidean straight lines, 1-dimensional circles and conic curves are all
considered Spaces. A Space hence naturally contains lower-dimensional Spaces.

Spaces do not have "hard" boundaries that "prevent" Points from moving across.
For example, half-planes or hemispheres are not considered Spaces. This means
that, algebraically, Spaces can be characterized by parametric equations with
unconstrained parameters.
"""


from collections.abc import Sequence
from typing import LiteralString

from .abc import ASpace, ASubSpace, AHalfSpace, AClosedSubSpace


__all__: Sequence[LiteralString] = ('ASpace',
                                    'ASubSpace', 'AHalfSpace', 'AClosedSubSpace')  # noqa: E501
