from PyAngle import Angle
from ezdxf.math import ConstructionLine, Vec2
from skspatial.objects import Vector
from numpy import sqrt
import ezdxf


def rotate2d(vec: Vector, ang: Angle):
    x = vec[0] * ang.cos() - vec[1] * ang.sin()
    y = vec[0] * ang.sin() + vec[1] * ang.cos()
    if vec.dimension == 3:
        return Vector([x, y, vec[3]])
    else:
        return Vector([x, y])


def length(vec: Vector) -> float:
    if vec.dimension == 3:
        return sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
    else:
        return sqrt(vec[0] ** 2 + vec[1] ** 2)


def cut_dxf(dxf_file, center: Vector, side: Vector):
    cutLine = ConstructionLine(center, side)
    pts = []
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()
    for e in msp:
        if e.dxftype() == 'LINE':
            byLine = ConstructionLine(e.dxf.start, e.dxf.end)
            pt = cutLine.intersect(byLine)
            if isinstance(pt, Vec2):
                pts.append(pt)
    if len(pts) != 0:
        pts.sort(key=lambda x: x.distance(center))
        return pts[0].distance(center)
    else:
        return None
