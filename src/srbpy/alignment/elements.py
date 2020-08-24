import numpy as np
import os

from .__cg import CG
from .__dmx import DMX
from .__pqx import PQX
from .__sqx import SQX


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
        """This is an example of a module level function.

        Function parameters should be documented in the ``Args`` section. The name
        of each parameter is required. The type and description of each parameter
        is optional, but should be included if not obvious.

        If ``*args`` or ``**kwargs`` are accepted,
        they should be listed as ``*args`` and ``**kwargs``.

        The format for a parameter is::

            name (type): description
                The description may span multiple lines. Following
                lines should be indented. The "(type)" is optional.

                Multiple paragraphs are supported in parameter
                descriptions.

        Args:
            param1 (int): The first parameter.
            param2 (:obj:`str`, optional): The second parameter. Defaults to None.
                Second line of description should be indented.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            bool: True if successful, False otherwise.

            The return type is optional and may be specified at the beginning of
            the ``Returns`` section followed by a colon.

            The ``Returns`` section may span multiple lines and paragraphs.
            Following lines should be indented to match the first line.

            The ``Returns`` section supports any reStructuredText formatting,
            including literal blocks::

                {
                    'param1': param1,
                    'param2': param2
                }

        Raises:
            AttributeError: The ``Raises`` section is a list of all exceptions
                that are relevant to the interface.
            ValueError: If `param2` is equal to `param1`.

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
