"""
路线元素的基本点
"""
class BPD(object):
    def __init__(self, pk, h, r):
        self.pk = pk
        self.elevation = h
        self.radius = r


class CGD(object):
    def __init__(self, pk, l_slope, r_slope):
        self.pk = pk
        self.l_slope = l_slope
        self.r_slope = r_slope


class RCD(object):
    def __init__(self, pk, h):
        self.pk = pk
        self.elevation = h
