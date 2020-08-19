import numpy as np
import os
from .pqx import PQX


class Align(object):
    name = ""
    _work_dir = ""
    _pqx=None
    _sqx=None
    _cg=None
    _hdx=None


    def __init__(self, name="", path=""):
        if os.path.exists(path) and os.path.isdir(path):
            self.name = name if name!="" else os.path.basename(path)
            self._work_dir = path
            self._pqx=PQX(os.path.join(path,self.name+".ICD"))
        else:
            raise FileNotFoundError("路线数据文件错误或未找到.")


class AlignCollection(object):
    pass
