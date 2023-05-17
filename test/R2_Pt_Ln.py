"""Test R2 Point & Line."""


from random import choice

from g.euclid.r2.point import Pt, PtAtInf
from g.euclid.r2.line import Ln, Ray, Seg

from g.session import Session, DEFAULT_SESSION

from g._util import debug


debug.ON: bool = True


s: Session = (Session()
              if choice((False, True))
              else DEFAULT_SESSION)


s.A = Pt(name='A')
print(s.A)
s.B = Pt(name='B')
print(s.B)
s.C = Pt(name='C')
print(s.C)
s.D = Pt(name='D')
print(s.D)


s.d = PtAtInf(s.D, name='d')
print(s.d)
s.d_ = PtAtInf(-s.D, name="d'")
print(s.d_)


s.lnAB = Ln(s.A, s.B)
print(s.lnAB)
s.lnAd = Ln(s.A, s.d)
print(s.lnAd)

s.lnCD = Ln(s.C, s.D)
print(s.lnCD)
s.lnCd = Ln(s.C, s.d)
print(s.lnCd)


s.rayAB = Ray(s.A, s.B)
print(s.rayAB)
s.rayAd = Ray(s.A, s.d)
print(s.rayAd)
s.rayAd_ = Ray(s.A, s.d_)
print(s.rayAd_)


s.segAB = Seg(s.A, s.B)
print(s.segAB)
