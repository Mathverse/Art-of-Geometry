"""Test R0 & R1 Point."""


from random import choice

from g.euclid._r0._point import PointR0
from g.euclid._r1.point import PointR1, PtAtInf

from g.session import Session, DEFAULT_SESSION

from g._util import debug


debug.ON: bool = True


s: Session = (Session()
              if choice((False, True))
              else DEFAULT_SESSION)


s.S = PointR0
print(s.S)

s.P = PointR1(name='P')
print(s.P)

s.p = PtAtInf
print(s.p)
