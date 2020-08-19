from skspatial.objects import Vector, Point
from enum import Enum
from PyAngle import Angle
import abc


class LeftRightEnum(Enum):
    NoneLR = 0
    Left = -1
    Right = 1


class EITypeID(Enum):
    NoType = 0
    Line = 1
    Arc = 2
    ZHY = 3
    YHZ = 4
    BigRtoSmallR = 5
    SmallRtoBigR = 6


class PQX(object):
    start_pk = 0
    start_point = Point([0, 0])

    def __init__(self, file=""):
        pass


class PQXElement(metaclass=abc.ABCMeta):
    '''
    平曲线元素基类
    '''
    typeid = EITypeID.NoType
    start_point = Point([0, 0])
    start_angle = Angle(degree=0)
    left_right = LeftRightEnum.NoneLR
    __length = 0
    __end_point = Point([0, 0])
    __end_angle = Angle(degree=0)

    def __init__(self, idd: EITypeID, pt: Point, st_angle: Angle, lr: LeftRightEnum):
        self.typeid = idd
        self.start_point = pt
        self.start_angle = st_angle
        self.left_right = lr

    @abc.abstractmethod
    def GetPointOnCurve(self, l):
        pass

    @property
    @abc.abstractmethod
    def length(self):
        return self.__length

    @property
    @abc.abstractmethod
    def end_angle(self):
        return self.end_angle

    @property
    @abc.abstractmethod
    def end_point(self):
        return self.end_point


class Straight(PQXElement):
    __length = 0

    def __init__(self, l, st, sdir, idd=EITypeID.Line, lr=LeftRightEnum.NoneLR):
        super().__init__(idd, st, sdir, lr)
        self.__length = l

    def GetPointOnCurve(self, l):
        x = l
        y = 0
        res = Vector([y, x])
        return self.start_point + Point([1, 1])
        pass

    @property
    def length(self):
        return  self.__length

    @property
    def end_angle(self):
        pass

    @property
    def end_point(self):
        pass
