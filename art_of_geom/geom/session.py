__all__ = 'Session', 'GLOBAL_SESSION'


from sympy.assumptions.assume import AssumptionsContext
from types import SimpleNamespace
from uuid import uuid4

from .abc import _GeometryEntityABC


class Session:
    def __init__(self, name: str = None):
        self.name = \
            name \
            if name \
            else str(uuid4())

        self.geometry_entities = {}

        self.sympy_assumptions = AssumptionsContext()

    def __repr__(self):
        return 'Geometry Session "{}"'.format(self.name)

    def __str__(self):
        return repr(self)

    def __setattr__(self, name, value):
        if isinstance(value, _GeometryEntityABC):
            value.session = self
            self.geometry_entities[name] = value

        else:
            object.__setattr__(self, name, value)

    def __setitem__(self, name, geometry_entity):
        assert isinstance(geometry_entity, _GeometryEntityABC)

        geometry_entity.session = self
        self.geometry_entities[name] = geometry_entity

    def __getattr__(self, name):
        return self.geometry_entities[name]

    def __getitem__(self, name):
        return self.geometry_entities[name]

    def __delattr__(self, name):
        del self.geometry_entities[name]

    def __delitem__(self, name):
        del self.geometry_entities[name]


# Global Geometry Session
GLOBAL_SESSION = Session(name='GLOBAL GEOMETRY SESSION')
