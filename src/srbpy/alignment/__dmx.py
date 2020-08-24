import copy
from .__base import RCD
import re
import numpy as np


class DMX(object):
    __RCDList = []

    def __init__(self, file=""):
        with open(file, 'r') as fid:
            text = fid.readlines()
        for i, line in enumerate(text):
            if line.startswith("//") or line == "":
                continue
            pt = RCD(0, 0)
            xx = re.split("\\s+", line.rstrip())
            pt.pk = float(xx[0])
            pt.elevation = float(xx[1])
            self.__RCDList.append(pt)
            self.__RCDList.sort(key=lambda x: x.pk)

    def get_bg(self, pk: float) -> float:
        if np.abs(pk) < 1e-3:
            pk = 0
        if pk < self.__RCDList[0].pk or pk > self.__RCDList[-1].pk:
            raise Exception("里程不在设计范围内.")
        elif pk in [a.pk for a in self.__RCDList]:
            for kk, a in enumerate(self.__RCDList):
                if a.pk == pk:
                    return a.elevation
        else:
            tmp = copy.deepcopy(self.__RCDList)
            pt = RCD(pk, 0)
            tmp.append(pt)
            tmp.sort(key=lambda x: x.pk)
            i0 = 0
            for i0, a in enumerate(tmp):
                if a.pk == pk:
                    break
            t1 = self.__RCDList[i0 - 1]
            t2 = self.__RCDList[i0]
            return t1.elevation + (t2.elevation - t1.elevation) / (t2.pk - t1.pk) * (pk - t1.pk)
