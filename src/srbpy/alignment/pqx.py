import abc
from enum import Enum
import numpy as np
from skspatial.objects import Point
from .ext import *


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

    @staticmethod
    def from_value(v: int):
        for item in EITypeID:
            if item.value == v:
                return item
            else:
                continue
        raise Exception("无法获取枚举.")


class PQXElement(metaclass=abc.ABCMeta):
    """
    平曲线元素基类
    """
    typeid = EITypeID.NoType
    start_point = Point([0, 0])
    start_angle = Angle(deg=0)
    left_right = LeftRightEnum.NoneLR
    __length = 0
    __end_point = Point([0, 0])
    __end_angle = Angle(deg=0)

    def __init__(self, idd: EITypeID, pt: Point, st_angle: Angle, lr: LeftRightEnum):
        self.typeid = idd
        self.start_point = pt
        self.start_angle = st_angle
        self.left_right = lr

    @abc.abstractmethod
    def get_point_on_curve(self, l_from_st):
        pass

    @property
    @abc.abstractmethod
    def length(self):
        pass

    @property
    @abc.abstractmethod
    def end_angle(self):
        pass

    @property
    @abc.abstractmethod
    def end_point(self):
        pass


class Straight(PQXElement):
    __length = 0

    def __init__(self, length, st, sdir, idd=EITypeID.Line, lr=LeftRightEnum.NoneLR):
        super().__init__(idd, st, sdir, lr)
        self.__length = length

    def get_point_on_curve(self, length):
        x = length
        y = 0
        res = rotate2d(Vector([y, x]), self.start_angle * -1)
        return self.start_point + res
        pass

    @property
    def length(self):
        return self.__length

    @property
    def end_angle(self):
        return self.start_angle

    @property
    def end_point(self):
        return self.get_point_on_curve(self.__length)


class Arc(PQXElement):
    __length = 0
    __radius = 0

    def __init__(self, r, length, st, sdir, direnum, idd=EITypeID.Arc):
        super().__init__(idd, st, sdir, direnum)
        self.__length = length
        self.__radius = r

    @property
    def length(self):
        return self.__length

    @property
    def radius(self):
        return self.__radius

    @property
    def end_point(self):
        return self.get_point_on_curve(self.__length)

    @property
    def end_angle(self):
        return self.start_angle + Angle.from_rad(self.__length / self.__radius) * float(self.left_right.value)

    def get_point_on_curve(self, l_from_st):
        rad = l_from_st / self.__radius
        x = self.__radius * np.sin(rad)
        y = self.left_right.value * self.__radius * (1 - np.cos(rad))
        res = rotate2d(Vector([y, x]), self.start_angle * -1)
        return self.start_point + res


class Sprial(PQXElement):

    def __init__(self, idd: EITypeID, a: float, sr: float, er: float, st: Point, sa: Angle, lr_dir: LeftRightEnum):
        super().__init__(idd, st, sa, lr_dir)
        self.__a = a
        self.__start_radius = sr
        self.__end_radius = er

    def __ab__(self, value: float, i: int, j: int, k: int, ll: int):
        rho_a = 1.0 / self.__start_radius
        rho_b = 1.0 / self.__end_radius
        const_a = rho_a
        const_b = (rho_b - rho_a) / (2.0 * self.length)
        return np.power(const_a, i) * np.power(const_b, j) / float(k) * np.power(value, ll)

    @staticmethod
    def eval_xy(R_st, A, l, idd):
        if idd in [3, 5]:
            x = l - l ** 3 / (6 * R_st ** 2) - l ** 4 / (8 * A ** 2 * R_st) + l ** 6 / (72 * A ** 2 * R_st ** 3) + l ** 5 * (A ** 4 - 3 * R_st ** 4) / (
                    120 * A ** 4 * R_st ** 4) + l ** 7 * (-A ** 4 + 45 * R_st ** 4) / (5040 * A ** 4 * R_st ** 6) - l ** 10 / (
                        2880 * A ** 6 * R_st ** 3) + l ** 8 * (-A ** 4 + 5 * R_st ** 4) / (1920 * A ** 6 * R_st ** 5) - l ** 11 / (
                        8448 * A ** 8 * R_st ** 2) + l ** 9 * (-2 * A ** 4 + R_st ** 4) / (3456 * A ** 8 * R_st ** 4) - l ** 12 / (
                        46080 * A ** 10 * R_st) - l ** 13 / (599040 * A ** 12)
            y = l ** 2 / (2 * R_st) - l ** 4 / (24 * R_st ** 3) + l ** 3 / (6 * A ** 2) - l ** 5 / (20 * A ** 2 * R_st ** 2) + l ** 6 * (
                    A ** 4 - 15 * R_st ** 4) / (720 * A ** 4 * R_st ** 5) + l ** 8 * (-A ** 4 + 105 * R_st ** 4) / (40320 * A ** 4 * R_st ** 7) + l ** 7 * (
                        A ** 4 - R_st ** 4) / (336 * A ** 6 * R_st ** 4) + l ** 9 * (-A ** 4 + 15 * R_st ** 4) / (12960 * A ** 6 * R_st ** 6) - l ** 12 / (
                        27648 * A ** 8 * R_st ** 3) + l ** 10 * (-2 * A ** 4 + 5 * R_st ** 4) / (19200 * A ** 8 * R_st ** 5) - l ** 13 / (
                        99840 * A ** 10 * R_st ** 2) + l ** 11 * (-10 * A ** 4 + 3 * R_st ** 4) / (126720 * A ** 10 * R_st ** 4) - l ** 14 / (
                        645120 * A ** 12 * R_st) - l ** 15 / (9676800 * A ** 14)
        elif idd in [4, 6]:
            x = l - l ** 3 / (6 * R_st ** 2) + l ** 4 / (8 * A ** 2 * R_st) - l ** 6 / (72 * A ** 2 * R_st ** 3) + l ** 5 * (A ** 4 - 3 * R_st ** 4) / (
                    120 * A ** 4 * R_st ** 4) + l ** 7 * (-A ** 4 + 45 * R_st ** 4) / (5040 * A ** 4 * R_st ** 6) + l ** 10 / (
                        2880 * A ** 6 * R_st ** 3) + l ** 8 * (A ** 4 - 5 * R_st ** 4) / (1920 * A ** 6 * R_st ** 5) - l ** 11 / (
                        8448 * A ** 8 * R_st ** 2) + l ** 9 * (-2 * A ** 4 + R_st ** 4) / (3456 * A ** 8 * R_st ** 4) + l ** 12 / (
                        46080 * A ** 10 * R_st) - l ** 13 / (599040 * A ** 12)
            y = l ** 2 / (2 * R_st) - l ** 4 / (24 * R_st ** 3) - l ** 3 / (6 * A ** 2) + l ** 5 / (20 * A ** 2 * R_st ** 2) + l ** 6 * (
                    A ** 4 - 15 * R_st ** 4) / (720 * A ** 4 * R_st ** 5) + l ** 8 * (-A ** 4 + 105 * R_st ** 4) / (40320 * A ** 4 * R_st ** 7) + l ** 7 * (
                        -A ** 4 + R_st ** 4) / (336 * A ** 6 * R_st ** 4) + l ** 9 * (A ** 4 - 15 * R_st ** 4) / (12960 * A ** 6 * R_st ** 6) - l ** 12 / (
                        27648 * A ** 8 * R_st ** 3) + l ** 10 * (-2 * A ** 4 + 5 * R_st ** 4) / (19200 * A ** 8 * R_st ** 5) + l ** 13 / (
                        99840 * A ** 10 * R_st ** 2) + l ** 11 * (10 * A ** 4 - 3 * R_st ** 4) / (126720 * A ** 10 * R_st ** 4) - l ** 14 / (
                        645120 * A ** 12 * R_st) + l ** 15 / (9676800 * A ** 14)
        else:
            raise Exception("缓和曲线类型错误.")
        return x, y

    def get_point_on_curve_old(self, l_from_st):
        x = l_from_st - self.__ab__(l_from_st, 2, 0, 6, 3) - self.__ab__(l_from_st, 1, 1, 4, 4) \
            - self.__ab__(l_from_st, 0, 2, 10, 5) + self.__ab__(l_from_st, 4, 0, 120, 5) + self.__ab__(l_from_st, 3, 1, 36, 6) \
            + self.__ab__(l_from_st, 2, 2, 28, 7) + self.__ab__(l_from_st, 1, 3, 48, 8) + self.__ab__(l_from_st, 0, 4, 216, 9)

        y = self.__ab__(l_from_st, 1, 0, 2, 2) + self.__ab__(l_from_st, 0, 1, 3, 3) - self.__ab__(l_from_st, 3, 0, 24, 4) \
            - self.__ab__(l_from_st, 2, 1, 10, 5) - self.__ab__(l_from_st, 1, 2, 12, 6) + self.__ab__(l_from_st, 5, 0, 720, 6) \
            - self.__ab__(l_from_st, 0, 3, 42, 7) + self.__ab__(l_from_st, 4, 1, 168, 7) + self.__ab__(l_from_st, 3, 2, 96, 8) \
            + self.__ab__(l_from_st, 2, 3, 108, 9)

        y *= self.left_right.value
        res = rotate2d(Vector([y, x]), self.start_angle * -1)
        return self.start_point + res

    def get_point_on_curve(self, l_from_st):
        x0, y0 = self.eval_xy(self.__start_radius, self.__a, l_from_st, self.typeid.value)
        y0 *= self.left_right.value
        res = rotate2d(Vector([float(y0), float(x0)]), self.start_angle * -1)
        return self.start_point + res

    @property
    def length(self):
        return np.abs(self.__a * self.__a / self.__start_radius - self.__a * self.__a / self.__end_radius)

    @property
    def end_angle(self):
        ang = Angle.from_rad(0.5 * self.__a ** 2 * np.abs(1.0 / (self.__start_radius ** 2) - 1.0 / (self.__end_radius ** 2)))
        return self.start_angle + ang * float(self.left_right.value)

    @property
    def end_point(self):
        return self.get_point_on_curve(self.length)


class PQX(object):
    start_pk = 0
    start_point = Point([0, 0])
    start_angle = Angle(deg=0)

    def __init__(self, file=""):
        cur_point = Point([0, 0])
        cur_angle = Angle(deg=0.0)
        elem_collection = []
        with open(file, 'r') as fid:
            text = fid.readlines()
        for i, line in enumerate(text):
            if i == 0:
                self.start_pk = float(line)
            elif i == 1:
                xx = line.split(',')
                start_x = float(xx[0])
                start_y = float(xx[1])
                start_ang_in_rad = float(xx[2])
                self.start_point = Point([start_y, start_x])
                self.start_angle = Angle(deg=start_ang_in_rad / np.pi * 180.0)
                cur_point = self.start_point
                cur_angle = self.start_angle
            else:
                xx = line.split(',')
                if line.startswith("//"):
                    continue
                elif len(xx) == 3 and int(xx[2]) == 0:
                    break
                else:
                    item = None
                    try:
                        type_id = int(xx[0])
                    except Exception:
                        raise Exception("无法解析元素1.")

                    if type_id == 1:  # 直线，长度，方位角
                        ll = float(xx[1])
                        item = Straight(ll, cur_point, cur_angle)
                    elif type_id == 2:
                        rr = float(xx[1])
                        ll = float(xx[2])
                        s_dir = LeftRightEnum.Left if int(xx[3]) == -1 else LeftRightEnum.Right
                        item = Arc(rr, ll, cur_point, cur_angle, s_dir)
                    elif type_id == 3:  #
                        idd = EITypeID.from_value(type_id)
                        aa = float(xx[1])
                        end_r = float(xx[2])
                        lr_dir = LeftRightEnum.Left if int(xx[3]) == -1 else LeftRightEnum.Right
                        item = Sprial(idd, aa, 1e39, end_r, cur_point, cur_angle, lr_dir)
                    elif type_id == 4:
                        idd = EITypeID.from_value(type_id)
                        aa = float(xx[1])
                        st_r = float(xx[2])
                        lr_dir = LeftRightEnum.Left if int(xx[3]) == -1 else LeftRightEnum.Right
                        item = Sprial(idd, aa, st_r, 1e39, cur_point, cur_angle, lr_dir)
                    elif type_id == 5 or type_id == 6:
                        idd = EITypeID.from_value(type_id)
                        aa = float(xx[1])
                        st_r = float(xx[2])
                        end_r = float(xx[3])
                        lr_dir = LeftRightEnum.Left if int(xx[4]) == -1 else LeftRightEnum.Right
                        item = Sprial(idd, aa, st_r, end_r, cur_point, cur_angle, lr_dir)
                    else:
                        raise Exception("读取ICD文件错误.")
                    elem_collection.append(item)
                    cur_angle = elem_collection[-1].end_angle
                    cur_point = elem_collection[-1].end_point
        self.__elem_collection = elem_collection

    @property
    def end_pk(self):
        if len(self.__elem_collection) == 0:
            return self.start_pk
        else:
            return self.start_pk + sum(item.length for item in self.__elem_collection)

    def get_dir(self, pk: float, delta: float = 0.00001):
        """
        获取任意里程切线单位向量
        Parameters
        ----------
        pk : float
            任意里程
        delta : float , optional
            精度值 , 默认0.00001

        Returns
        -------
        out : list
            切线单位向量坐标值
        """
        x0 = self.get_coordinate(pk - delta)[0]
        y0 = self.get_coordinate(pk - delta)[1]
        x1 = self.get_coordinate(pk + delta)[0]
        y1 = self.get_coordinate(pk + delta)[1]
        ll = np.sqrt((x0 - x1) * (x0 - x1) + (y0 - y1) * (y0 - y1))
        return [(x1 - x0) / ll, (y1 - y0) / ll]

    def get_coordinate(self, pk: float):
        """
        返回任意里程坐标.
        Parameters
        ----------
        pk : float
            里程桩号.
        Returns
        -------
        out : list
            大地坐标
        """
        if pk < self.start_pk:
            return self.get_coordinate(self.start_pk)
        elif pk <= self.end_pk:
            tmp = [item.length for item in self.__elem_collection]
            len_sum_up = [self.start_pk]
            for ll in tmp:
                len_sum_up.append(len_sum_up[-1] + ll)
            aa = 0
            for aa, val in enumerate(len_sum_up):
                if val > pk:
                    break
            aa = aa - 1

            if pk == self.end_pk:
                pre_pk = len_sum_up[-2]
                # nex_pk = len_sum_up[-1]
            else:
                pre_pk = len_sum_up[aa]
                # nex_pk = len_sum_up[aa + 1]
            ll = pk - pre_pk
            res = self.__elem_collection[aa].get_point_on_curve(ll)
            return res[0], res[1]

    def get_station_by_point(self, x0: float, y0: float, step: int = 20, delta: float = 1e-9) -> float:
        """
        根据单点获得正交桩号(可能多解)
        Parameters
        ----------
        x0 : float
            坐标X
        y0 : float
            坐标Y
        step : int
            步长，越大精度越高，但求解时间增加
        delta : float
            精度

        Returns
        -------
        out : float
            返回对应桩号
        """
        res = []
        dk = (self.end_pk - self.start_pk) / step
        target = Point([x0, y0])
        for i in range(step):
            if i == 17:
                test = True
            k1 = self.start_pk + dk * i
            k2 = k1 + dk
            k0, err = self.__binary_test__(k1, k2, target, delta)
            res.append([k0, err])
        res.sort(key=lambda x: x[1])
        return res[0][0]

    def get_side(self, x0: float, y0: float) -> int:
        pk_center = self.get_station_by_point(x0, y0)
        center = Point(list(self.get_coordinate(pk_center)))
        v_dir = Vector(list(self.get_dir(pk_center)))
        v_cross = Point([x0, y0]) - center
        if length(v_cross) == 0:
            return 0
        else:
            ang = Angle.from_rad(v_dir.angle_signed(v_cross))
            if ang.to_degrees() < 180:
                return -1
            else:
                return 1

    def __solve_closer__(self, pk1: float, pk2: float, pt: Point):
        """
        二分法
        Parameters
        ----------
        pk1 : float
            里程起点
        pk2 : float
            里程终点
        pt : Point
            逼近点

        Returns
        -------
        out : float , float , float
            迭代下限,上限,评价值
        """
        assert pk1 <= pk2
        p1 = Point(list(self.get_coordinate(pk1)))
        p2 = Point(list(self.get_coordinate(pk2)))
        if p1.distance_point(pt) < p2.distance_point(pt):
            return pk1, 0.5 * (pk1 + pk2), p1.distance_point(pt)
        else:
            return 0.5 * (pk1 + pk2), pk2, p2.distance_point(pt)

    def __binary_test__(self, pk1: float, pk2: float, pt: Point, delta: float) -> tuple:
        """

        Parameters
        ----------
        pk1
        pk2
        pt
        delta

        Returns
        -------
        out : (r,dist)
            最优解,误差
        """
        mid = 0
        while np.abs(pk1 - pk2) > delta:
            pk1, pk2, dist = self.__solve_closer__(pk1, pk2, pt)
            mid = 0.5 * (pk1 + pk2)
        res1 = mid
        pk1, pk2, dist = self.__solve_closer__(res1, res1, pt)
        return res1, dist
