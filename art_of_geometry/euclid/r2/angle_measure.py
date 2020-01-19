from sympy.functions.elementary.trigonometric import atan2

from .point import Point


def ray_directed_angle_measure(point_0: Point, point_1: Point):
    return atan2(y=point_1.y - point_0.y,
                 x=point_1.x - point_0.x)
