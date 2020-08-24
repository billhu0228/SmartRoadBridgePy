from PyAngle import Angle
from skspatial.objects import Vector
from numpy import sqrt

def rotate2d(vec:Vector, ang:Angle):
    x = vec[0] * ang.cos() - vec[1] * ang.sin()
    y = vec[0] * ang.sin() + vec[1] * ang.cos()
    if vec.dimension==3:
        return Vector([x,y,vec[3]])
    else:
        return Vector([x,y])


def length(vec:Vector)->float:
    if vec.dimension==3:
        return sqrt(vec[0]**2+vec[1]**2+vec[2]**2)
    else:
        return sqrt(vec[0]**2+vec[1]**2)