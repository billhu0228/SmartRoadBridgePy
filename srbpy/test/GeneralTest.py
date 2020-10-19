from srbpy.alignment import Align
from numpy import pi, cos

def AbutInfo(PK, Al, dx):
    Ele = Al.get_elevation(PK)
    Lpk, Rpk = Al.get_lrpk(PK, 2.0 / 3.0 * pi)
    LEle = Al.get_elevation(Lpk) - Al.get_width(Lpk)[0] * Al.get_cross_slope(Lpk)[0]
    REle = Al.get_elevation(Rpk) + Al.get_width(Rpk)[1] * Al.get_cross_slope(Rpk)[1]
    LenL = Al.get_width(PK)[0] / cos(1.0 / 6.0 * pi)
    LenR = Al.get_width(PK)[1] / cos(1.0 / 6.0 * pi)
    print("  %s：中心桩号%.3f\n\t设计高程：%.3f" % (Al.name, PK, Ele))
    print("\t支座桩号：%.3f，支座处桥面高程：%.3f" % (PK + dx, Al.get_elevation(PK + dx)))
    print("\t纵坡：%.2f%%" % (Al.get_slope(PK) * 100.0))
    print("\t左侧路边高程：%.3f，右侧路边高程：%.3f" % (LEle, REle))
    print("\t桥台左坡：%.2f%%，桥台右坡：%.2f%%" % ((Ele - LEle) / LenL * 100.0, (REle - Ele) / LenR * 100.0))

if __name__ == "__main__":
    M1K = Align(path=r"G:\20191213-肯尼亚高架桥施工图设计(19406)\01 前方资料\EI Data\00-MainLine\M1K-0312")
    M1K.set_width(28.6)
    A8L = Align(path=r"G:\20191213-肯尼亚高架桥施工图设计(19406)\01 前方资料\EI Data\09-A8\A8L2")
    A8L.set_width(11.5)
    AbutInfo(11658, M1K, +0.540)
    AbutInfo(11688, M1K, -0.540)
    AbutInfo(323.67, A8L, +0.540)
    AbutInfo(353.67, A8L, -0.540)

    for a in range(9):
        qm=M1K.get_surface_elevation(11658+0.540,-(a-4)*(3.1625/cos(1.0/6.0*pi)),2.0/3.0*pi)
        print("%i#垫石 顶面标高：%.3f"%(a+1,qm-0.07-1.7-0.05-0.11))

    for a in range(9):
        qm=M1K.get_surface_elevation(11688-0.540,+(a-4)*(3.1625/cos(1.0/6.0*pi)),2.0/3.0*pi)
        print("%i#垫石 顶面标高：%.3f"%(a+1,qm-0.07-1.7-0.05-0.11))