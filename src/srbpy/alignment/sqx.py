import copy
from .base import BPD
import re
import numpy as np


class SQX(object):
    __BPDList = []

    def __init__(self, file=""):
        with open(file, 'r') as fid:
            text = fid.readlines()
        for i, line in enumerate(text):
            if line.startswith("//") or line == "":
                continue
            pt = BPD(0, 0, 0)
            xx = re.split("\\s+", line.rstrip())
            pt.pk = float(xx[0])
            pt.elevation = float(xx[1])
            if len(xx) == 3:
                pt.radius = float(xx[2])
            else:
                pt.radius = -1
            self.__BPDList.append(pt)
            self.__BPDList.sort(key=lambda x: x.pk)

    def __get_ab(self, k: int):
        cur_bpd = self.__BPDList[k]
        if k == 0:
            i2 = (self.__BPDList[k + 1].elevation - cur_bpd.h) / (self.__BPDList[k + 1].pk - cur_bpd.pk)
            i1 = -i2
        elif k == len(self.__BPDList) - 1:
            i1 = (cur_bpd.elevation - self.__BPDList[k - 1].elevation) / (cur_bpd.pk - self.__BPDList[k - 1].pk)
            i2 = -i1
        else:
            i1 = (cur_bpd.elevation - self.__BPDList[k - 1].elevation) / (cur_bpd.pk - self.__BPDList[k - 1].pk)
            i2 = (self.__BPDList[k + 1].elevation - cur_bpd.elevation) / (self.__BPDList[k + 1].pk - cur_bpd.pk)
        w = i2 - i1
        t = cur_bpd.radius * np.abs(w) * 0.5
        begin = cur_bpd.pk - t
        end = cur_bpd.pk + t
        direct = -1 if w < 0 else 1
        return begin, end, direct

    def get_bg(self, pk: float):
        if np.abs(pk) < 1e-3:
            pk = 0
        if pk < self.__BPDList[0].pk or pk > self.__BPDList[-1].pk:
            raise Exception("里程不在设计范围内.")
        elif pk in [a.pk for a in self.__BPDList]:
            if pk == self.__BPDList[0].pk:
                res = self.__BPDList[0].elevation
            elif pk == self.__BPDList[-1].pk:
                res = self.__BPDList[-1].elevation
            else:
                res = (self.get_bg(pk + 0.000001) + self.get_bg(pk - 0.000001)) * 0.5
        else:
            tmp = copy.deepcopy(self.__BPDList)
            pt = BPD(pk, 0, 0)
            tmp.append(pt)
            tmp.sort(key=lambda x: x.pk)
            kk = 0
            for kk, a in enumerate(tmp):
                if a.pk == pk:
                    break
            cc = (self.__BPDList[kk].elevation - self.__BPDList[kk - 1].elevation) / (self.__BPDList[kk].pk - self.__BPDList[kk - 1].pk)
            y0 = (pk - self.__BPDList[kk - 1].pk) * cc + self.__BPDList[kk - 1].elevation
            begin_a, end_a, dir_a = self.__get_ab(kk - 1)
            begin_b, end_b, dir_b = self.__get_ab(kk)
            if pk < end_a:
                dy = (end_a - pk) ** 2 / self.__BPDList[kk - 1].radius * 0.5 * dir_a
            elif pk >= begin_b:
                dy = (pk - begin_b) ** 2 / self.__BPDList[kk].radius * 0.5 * dir_b
            else:
                dy = 0
            res = y0 + dy
        return res

    def get_zp(self, pk: float):
        zp1 = (self.get_bg(pk) - self.get_bg(pk - 0.001)) / 0.001 * 100.0
        zp2 = (self.get_bg(pk + 0.001) - self.get_bg(pk)) / 0.001 * 100.0
        return (zp1 + zp2) * 0.5 * 0.01
