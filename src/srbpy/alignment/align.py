# -*- coding : utf-8-*-
import json
import os
from dataclasses import dataclass, field

import ezdxf
from PyAngle import Angle
from numpy import pi, cos, sin
from ezdxf.math import Vector, Vec2

from .align_cg import CG
from .align_dmx import DMX
from .align_pqx import PQX
from .align_sqx import SQX
from ..extension import cut_dxf, signed_angle_between
from ..server import Base, Column, String, Text


class Align(Base):
    # 增加ORM映射 -- Bill 2020/11/18
    __tablename__ = "ei_tbl"
    name = Column('name', String(10), primary_key=True)
    _fICD = Column('ICD', Text, nullable=True)
    _fSQX = Column('SQX', Text, nullable=True)
    _fDMX = Column('DMX', Text, nullable=True)
    _fCG = Column('CG', Text, nullable=True)
    _fHDX = Column('HDX', Text, nullable=True)
    #

    _work_dir = ""
    _pqx = None
    _sqx = None
    _dmx = None
    _cg = None
    _hdx = None
    _left_w = 0.0
    _right_w = 0.0
    _width_dxf = ""

    def __init__(self, name, path):
        """
        EICAD路线类

        Args:
            path(str): 路线数据包文件根目录
            name(str): 可选, 如为空则使用path参数的目录名称

        """
        if os.path.exists(path) and os.path.isdir(path):
            basename = os.path.basename(path)
            self.name = name if name != "" else basename
            self._work_dir = path
            self._pqx = PQX(os.path.join(path, basename + ".ICD"))
            self._sqx = SQX(os.path.join(path, basename + ".SQX"))
            self._dmx = DMX(os.path.join(path, basename + ".DMX"))
            self._cg = CG(os.path.join(path, basename + ".CG"))
            # self._hdx=HDX()
            self.start_pk = self._pqx.start_pk
            self.end_pk = self._pqx.end_pk
        else:
            raise FileNotFoundError("路线数据文件错误或未找到.")

        # 增加ORM映射 -- Bill 2020/11/18
        self._fICD = self._pqx.Text
        self._fSQX = self._sqx.Text
        self._fDMX = self._dmx.Text
        self._fCG = self._cg.Text

    def get_station_by_point(self, x0: float, y0: float, step: int = 10, delta: float = 1e-9) -> float:
        """
        根据单点获得正交桩号(可能多解)。

        Args:
            x0 (float): 坐标X
            y0 (float): 坐标y
            step (int): 步长，越大精度越高，但求解时间增加
            delta (float): 精度

        Returns:
            float: 返回对应桩号

        """
        return self._pqx.get_station_by_point(x0, y0, step, delta)

    def get_station_by_point2(self, x0: float, y0: float, x1: float, y1: float,
                              delta: float = 1e-6) -> float:
        """
        根据两点获得两点所在直线与路线交点。

        Args:
            x0:(float): 点1 坐标X
            y0:(float): 点1 坐标Y
            x1:(float): 点2 坐标X
            y1:(float): 点2 坐标Y
            delta: 误差，default=1e-6.

        Returns:
            交点桩号.

        """
        return self._pqx.get_station_by_point2(x0, y0, x1, y1, delta)

    def get_direction(self, pk: float, delta: float = 1e-6):
        """
        获取前进方向向量。

        Args:
            pk (float): 里程桩号
            delta (float): 可选, 精度,默认值1e-6

        Returns:
            [float,float]: 方向向量坐标(已单位化)。


        """
        return [self._pqx.get_dir(pk, delta)[0], self._pqx.get_dir(pk, delta)[1]]

    def get_coordinate(self, pk: float):
        """
        获取任意桩号坐标。

        Args:
            pk (float): 里程桩号

        Returns:
            [float,float]: 大地坐标。

        """

        return [self._pqx.get_coordinate(pk)[0], self._pqx.get_coordinate(pk)[1]]

    def get_side(self, x0: float, y0: float):
        """
        获取任意点在中心线的左右位置。

        Args:
            x0 (float): 任意点x坐标
            y0 (float): 任意点y坐标

        Returns:
            int :
                -1 : 左侧
                0 : 点在中心线上
                +1: 右侧
        """
        return self._pqx.get_side(x0, y0)

    def get_elevation(self, pk: float) -> float:
        """
        获取任意点标高。

        Args:
            pk (float): 里程桩号Fuck

        Returns:
            float: 标高

        """
        return self._sqx.get_bg(pk)

    def get_surface_elevation(self, pk: float, dist: float, angle: float = 0.5 * pi) -> float:
        """
        获取任意里程，斜距下桥面标高.

        Args:
            pk (float): 里程桩号
            dist (float): 斜距, 向右为正, 可大于桥面宽度
            angle (float): 斜交角, 正交时为0.5*pi, 逆时针为正, 默认值为0.5*pi.

        Returns:
            float : 设计高程
        """

        center = Vec2(*self.get_coordinate(pk))
        norm_l = Vec2(self.get_direction(pk))
        pt = center - norm_l.rotate(angle) * dist
        pk_new = self.get_station_by_point(pt[0], pt[1])
        center_new = Vec2(self.get_coordinate(pk_new))
        dist_new = self.get_side(pt[0], pt[1]) * pt.distance(center_new)
        ele_new = self.get_elevation(pk_new)
        hp = self.get_cross_slope(pk_new)[0] if self.get_side(pt[0], pt[1]) < 0 else self.get_cross_slope(pk_new)[1]
        return ele_new + dist_new * hp

    def get_ground_elevation(self, pk: float, dist: float) -> float:
        """
        获取任意里程处地面标高。

        Args:
            pk (float): 里程桩号
            dist (float): 斜距, 向右为正

        Returns:
            float: 标高
        """
        return self._dmx.get_bg(pk)

    def get_slope(self, pk: float) -> float:
        """
        获取任意里程处纵坡。

        Args:
            pk (float): 里程桩号

        Returns:
            float: 纵坡
        """
        return self._sqx.get_zp(pk)

    def get_cross_slope(self, pk: float, angle: float = 0.5 * pi):
        """
        获取任意里程处纵坡。

        Args:
            pk (float): 里程桩号
            angle (float): 斜交角, 正交时为0.5*pi, 逆时针为正, 默认值为0.5*pi.

        Returns:
            (float,float) : 左横坡,右横坡
        """
        if angle == 0.5 * pi:
            return self._cg.get_hp(pk)
        else:
            c_elevation = self.get_elevation(pk)
            left_pk, right_pk = self.get_lrpk(pk, angle)
            left_w, right_w = self.get_width(pk, angle)
            left_elevation = c_elevation - self.get_width(left_pk)[0] * self.get_cross_slope(left_pk)[0]
            right_elevation = c_elevation + self.get_width(right_pk)[1] * self.get_cross_slope(right_pk)[1]
            return (c_elevation - left_elevation) / left_w, (right_elevation - c_elevation) / right_w

    def set_width(self, width: float = 0, lw: float = 0, rw: float = 0, dxf_path: str = ""):
        """
        配置路线宽度。

        参数： width (float): 宽度，适用于等宽桥,左右等宽

        参数： lw 路线左宽， rw 路线右宽，适用于等宽桥，左右不等宽

        参数： dxf_path (str): dxf格式的宽度文件

        Returns:
            None

        """
        if width != 0:
            self._left_w = 0.5 * width
            self._right_w = 0.5 * width
        elif lw != 0 or rw != 0:
            self._left_w = lw
            self._right_w = rw
        elif dxf_path != "":
            self._left_w = 0.0
            self._right_w = 0.0
            # self._width_dxf = dxf_path
            self._width_dxf = ezdxf.readfile(dxf_path)
        else:
            raise Exception("宽度参数输入有误.")

    def get_width(self, pk: float, angle: float = 0.5 * pi):
        """
        获取任意里程桥面设计宽度

        Args:
            pk (float): 里程桩号
            angle (float): 斜交角, 正交时为0.5*pi, 逆时针为正, 默认值为0.5*pi.

        Returns:
            (float,float) : 左宽,右宽
        """

        if self._right_w == 0 and self._left_w == 0:
            if self._width_dxf == "":
                raise Exception("未定义任何宽度信息.")
            else:
                cc = Vector(*self.get_coordinate(pk))
                left = cc + Vector(*self.get_direction(pk)).rotate(angle) * 100.0
                right = cc + Vector(*self.get_direction(pk)).rotate(angle) * -100.0
                lw, vecL = cut_dxf(self._width_dxf, cc, left)
                rw, vecR = cut_dxf(self._width_dxf, cc, right)
                if isinstance(lw, float) and isinstance(rw, float):
                    return lw, rw
                else:
                    raise Exception("宽度文件在里程%.3f处无法推断宽度." % pk)
        else:
            if angle == 0.5 * pi:
                return self._left_w, self._right_w
            else:
                lpt, rpt = self.get_extreme(pk, angle)
                center = Vec2(*self.get_coordinate(pk))
                return center.distance(lpt), center.distance(rpt)

    def get_extreme(self, pk: float, angle: float = 0.5 * pi):
        """
        获取任意桩号沿任意偏角的左右桥面极点

        Args:
            pk (float): 里程桩号
            angle (float): 斜交角, 正交时为0.5*pi, 逆时针为正, 默认值为0.5*pi.

        Returns:
            Vec2,Vec2 : 左侧边缘坐标，右侧边缘坐标

        """
        pkl, pkr = self.get_lrpk(pk, angle)
        norm_l = Vec2(self.get_direction(pkl))
        width_l = self.get_width(pkl)[0]
        pt_left = Vec2(*self.get_coordinate(pkl)) + norm_l.rotate(0.5 * pi) * width_l
        norm_r = Vec2(self.get_direction(pkr))
        width_r = self.get_width(pkr)[1]
        pt_right = Vec2(*self.get_coordinate(pkr)) - norm_r.rotate(0.5 * pi) * width_r
        return pt_left, pt_right

    def get_lrpk(self, pk: float, angle: float = 0.5 * pi):
        """
        获取任意里程桥面左右侧对应桩号

        Args:
            pk (float): 里程桩号
            angle (float): 斜交角, 正交时为0.5*pi, 逆时针为正, 默认值为0.5*pi.

        Returns:
            (float,float) : 左侧边线桩号,右侧边线桩号

        """
        if self._right_w == 0 and self._left_w == 0:
            if self._width_dxf == "":
                raise Exception("未定义任何宽度信息.")
            else:
                cc = Vector(*self.get_coordinate(pk))
                left = cc + Vector(*self.get_direction(pk)).rotate(angle) * 100.0
                right = cc + Vector(*self.get_direction(pk)).rotate(angle) * -100.0
                lw, ptl = cut_dxf(self._width_dxf, cc, left)
                rw, ptr = cut_dxf(self._width_dxf, cc, right)
                if isinstance(lw, float) and isinstance(rw, float):
                    pkl = self.get_station_by_point(ptl[0], ptl[1])
                    pkr = self.get_station_by_point(ptr[0], ptr[1])
                    return pkl, pkr
                else:
                    raise Exception("宽度文件在里程%.3f处无法推断宽度." % pk)
        else:
            pkl = self.binary_search(
                range=[max(self.start_pk, pk - 100), min(self.end_pk, pk + 100)],
                precision=1e-10,
                center=pk,
                tar_ang=angle
            )
            pkr = self.binary_search(
                range=[max(self.start_pk, pk - 100), min(self.end_pk, pk + 100)],
                precision=1.0e-10,
                center=pk,
                tar_ang=angle + pi
            )
            return pkl, pkr

    def _better(self, pk1, pk2, center: float, tar_ang: float):
        """
        求解center至边线夹角更接近tar_ang的位置

        Args:
            pk1 (float): 桩号1
            pk2 (float): 桩号2
            center (float): 中心点桩号
            tar_ang: 弧度，目标夹角，左侧为逆时针小于pi，右侧大于pi

        Returns:

        """
        norm = Vec2(*self.get_direction(center))
        ccpt = Vec2(*self.get_coordinate(center))
        pkm = (pk1 + pk2) * 0.5
        wl1, wr1 = self.get_width(pk1)
        wlm, wrm = self.get_width(pkm)
        wl2, wr2 = self.get_width(pk2)
        if tar_ang <= pi:  # 左侧目标角度
            find_dir = 0.5 * pi
            w1 = wl1
            wm = wlm
            w2 = wl2
        else:
            find_dir = -0.5 * pi
            w1 = wr1
            wm = wrm
            w2 = wr2

        pt1 = Vec2(*self.get_coordinate(pk1)) + Vec2(*self.get_direction(pk1)).rotate(find_dir) * w1
        ptm = Vec2(*self.get_coordinate(pkm)) + Vec2(*self.get_direction(pkm)).rotate(find_dir) * wm
        pt2 = Vec2(*self.get_coordinate(pk2)) + Vec2(*self.get_direction(pk2)).rotate(find_dir) * w2

        val1 = signed_angle_between(norm, pt1 - ccpt)
        valm = signed_angle_between(norm, ptm - ccpt)
        val2 = signed_angle_between(norm, pt2 - ccpt)
        if (val1 - tar_ang) * (val2 - tar_ang) < 0:
            if (val1 - tar_ang) * (valm - tar_ang) < 0:
                return pk1, pkm
            else:
                return pkm, pk2
        else:
            return None

    def binary_search(self, range, precision, **kwargs):
        st = range[0]
        ed = range[-1]
        while abs(ed - st) > precision:
            st, ed = self._better(st, ed, center=kwargs["center"], tar_ang=kwargs["tar_ang"])
        return (st + ed) * 0.5

    def serialize(self, step: float = 100):
        """
        路线对象序列化。

        Args:
            step (float) : 步长，默认100m

        Returns:

        """
        listPt = []
        pk = self.start_pk
        while pk < self.end_pk:
            x, y = self.get_coordinate(pk)
            z = self.get_elevation(pk)
            z0 = self.get_ground_elevation(pk)
            pos = {"PK": pk, "X": x, "Y": y, "Z": z, "Z0": z0}
            listPt.append(pos)
            pk += step
        dict = {
            "Position": listPt,
            "Width": [self._left_w, self._right_w],
            "Width_dxf": self._width_dxf,
        }
        return json.dumps(dict)
