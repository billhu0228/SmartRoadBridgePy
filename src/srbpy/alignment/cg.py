import copy

from .base import CGD
import re
import numpy as np


class CG(object):
    __CGDList = []

    def __init__(self, file=""):
        is_read_first = False
        with open(file, 'r') as fid:
            text = fid.readlines()
        for i, line in enumerate(text):
            if line.startswith("//") or line == "":
                continue
            xx = re.split("\\s+", line.rstrip())
            if not is_read_first:
                self.__TypeID = int(xx[0])
                self.__dtl = float(xx[1])  # 超高旋转轴至左右边线距离
                self.__dtr = float(xx[2])
                self.__isSlop = float(xx[3])
                self.__jd1 = int(xx[4])
                self.__axi = float(xx[5])
                self.__jd2 = int(xx[6])
                is_read_first = True
                if self.__axi != 0 or self.__jd2 != 2:
                    raise Exception("超高数据类型超过已知.")
            else:
                pt = CGD(0, 0, 0)
                if len(xx) == 3:
                    pt.pk = float(xx[0])
                    pt.l_slope = float(xx[1])
                    pt.r_slope = float(xx[2])
                else:
                    pt.pk = float(xx[0])
                    pt.l_slope = float(xx[1])
                    pt.r_slope = float(xx[1])
                self.__CGDList.append(pt)
                self.__CGDList.sort(key=lambda x: x.pk)

    def get_hp(self, pk: float):
        if np.abs(pk) < 1e-4:
            pk = 0
        if pk < self.__CGDList[0].pk or pk > self.__CGDList[-1].pk:
            raise Exception("里程不在设计范围内.")
        elif pk in [a.pk for a in self.__CGDList]:
            if pk == self.__CGDList[0].pk:
                res = [self.__CGDList[0].l_slope, self.__CGDList[0].r_slope]
            elif pk == self.__CGDList[-1].pk:
                res = [self.__CGDList[-1].l_slope, self.__CGDList[-1].r_slope]
            else:
                ls = (self.get_hp(pk + 0.000001)[0] + self.get_hp(pk - 0.000001)[0]) * 0.5
                rs = (self.get_hp(pk + 0.000001)[1] + self.get_hp(pk - 0.000001)[1]) * 0.5
                res = [ls, rs]
        else:
            tmp = copy.deepcopy(self.__CGDList)
            pt = CGD(pk, 0, 0)
            tmp.append(pt)
            tmp.sort(key=lambda x: x.pk)
            kk = 0
            for kk, a in enumerate(tmp):
                if a.pk == pk:
                    break
            cc_left = (self.__CGDList[kk].l_slope - self.__CGDList[kk - 1].l_slope) / \
                      (self.__CGDList[kk].pk - self.__CGDList[kk - 1].pk)
            cc_right = (self.__CGDList[kk].r_slope - self.__CGDList[kk - 1].r_slope) / \
                       (self.__CGDList[kk].pk - self.__CGDList[kk - 1].pk)
            if cc_left * cc_right > 0 and cc_left != cc_right:  # 超高等待
                if np.abs(cc_left) > np.abs(cc_right):  # 左插值，右等待
                    ls = (pk - tmp[kk - 1].pk) * cc_left + tmp[kk - 1].l_slope
                    if cc_right > 0:
                        rs = min(ls, tmp[kk + 1].r_slope)
                    else:
                        rs = min(ls, tmp[kk - 1].r_slope)
                else:  # 右差值，左等待
                    rs = (pk - tmp[kk - 1].pk) * cc_right + tmp[kk - 1].r_slope
                    if cc_left > 0:
                        ls = max(rs, tmp[kk - 1].l_slope)
                    else:
                        ls = max(rs, tmp[kk + 1].l_slope)
                res = [ls, rs]
            else:  # 直接差值
                ls = (pk - self.__CGDList[kk - 1].pk) * cc_left + self.__CGDList[kk - 1].l_slope
                rs = (pk - self.__CGDList[kk - 1].pk) * cc_right + self.__CGDList[kk - 1].r_slope
                res = [ls, rs]
        return res[0] * 0.01, res[1] * 0.01
