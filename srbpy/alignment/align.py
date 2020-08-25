import os
from srbpy.alignment.align_cg import CG
from srbpy.alignment.align_dmx import DMX
from srbpy.alignment.align_pqx import PQX
from srbpy.alignment.align_sqx import SQX


class Align(object):
    name = ""
    _work_dir = ""
    _pqx = None
    _sqx = None
    _dmx = None
    _cg = None
    _hdx = None

    def __init__(self, path, name=""):
        if os.path.exists(path) and os.path.isdir(path):
            self.name = name if name != "" else os.path.basename(path)
            self._work_dir = path
            self._pqx = PQX(os.path.join(path, self.name + ".ICD"))
            self._sqx = SQX(os.path.join(path, self.name + ".SQX"))
            self._dmx = DMX(os.path.join(path, self.name + ".DMX"))
            self._cg = CG(os.path.join(path, self.name + ".CG"))
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
            [float,float]: 大地坐标。

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
