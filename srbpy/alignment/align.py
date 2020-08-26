import os

from numpy import pi
from ezdxf.math import Vector

from srbpy.alignment.align_cg import CG
from srbpy.alignment.align_dmx import DMX
from srbpy.alignment.align_pqx import PQX
from srbpy.alignment.align_sqx import SQX
from srbpy.extension import cut_dxf


class Align(object):
    _work_dir = ""
    _pqx = None
    _sqx = None
    _dmx = None
    _cg = None
    _hdx = None
    _left_w = 0.0
    _right_w = 0.0
    _width_dxf = ""

    def __init__(self, path, name=""):
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
        else:
            raise FileNotFoundError("路线数据文件错误或未找到.")

    def get_station_by_point(self, x0: float, y0: float, step: int = 20, delta: float = 1e-9) -> float:
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

    def get_direction(self, pk: float, delta: float = 1e-6):
        """
        获取前进方向向量。

        Args:
            pk (float): 里程桩号
            delta (float): 可选, 精度,默认值1e-6

        Returns:
            [float,float]: 方向向量坐标(已单位化)。


        """
        return self._pqx.get_dir(pk, delta)

    def get_coordinate(self, pk: float):
        """
        获取任意桩号坐标。

        Args:
            pk (float): 里程桩号

        Returns:
            (float,float): 大地坐标。

        """

        return self._pqx.get_coordinate(pk)

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

    def get_ground_elevation(self, pk: float) -> float:
        """
        获取任意里程处地面标高。

        Args:
            pk (float): 里程桩号

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

    def get_cross_slope(self, pk: float):
        """
        获取任意里程处纵坡。

        Args:
            pk (float): 里程桩号

        Returns:
            (float,float) : 左横坡,右横坡
        """
        return self._cg.get_hp(pk)

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
            self._width_dxf = dxf_path
        else:
            raise Exception("宽度参数输入有误.")

    def get_width(self, pk: float):
        """
        获取任意里程桥面设计宽度

        Args:
            pk (float): 里程桩号

        Returns:
            (float,float) : 左宽,右宽
        """

        if self._right_w == 0 and self._left_w == 0:
            if self._width_dxf == "":
                raise Exception("未定义任何宽度信息.")
            else:
                cc = Vector(*self.get_coordinate(pk))
                left = cc + Vector(*self.get_direction(pk)).rotate(0.5 * pi) * 100.0
                right = cc + Vector(*self.get_direction(pk)).rotate(0.5 * pi) * -100.0
                lw = cut_dxf(self._width_dxf, cc, left)
                rw = cut_dxf(self._width_dxf, cc, right)
                if isinstance(lw, float) and isinstance(rw, float):
                    return lw, rw
                else:
                    raise Exception("宽度文件在里程%.3f处无法推断宽度." % pk)
        else:
            return self._left_w, self._right_w
