from srbpy.model import Model, Bridge
# from srbpy.stdlib import std_Piers, std_Beams, std_Foundations, std_Abutments  # 导入自带标准结构库
# from srbpy.stdlib import std_Joint, std_Bearing  # 导入支座伸缩缝
from srbpy.stdlib.std_piers import *

# ---------------------------------------------------------------
# 初始化环境
md = Model()
# 导入路线资源
m1k = md.load_align(path="00-MainLine/M1K-0312", name="M1K")
m2k = md.load_align(path="00-MainLine/M2K-0312", name="M2K")
m2k.set_width(width=21.6)  # 等宽桥
m1k.set_width(dxf_path="00-MainLine/主线边线.dxf")  # 指定边线文件
# 导入桥梁资源
Br1 = Bridge(name="SEC201", )

md.bridges["SEC201"] = Br1  # 或者可以用下面这种方法添加桥梁布置
md.load_bridge(obj=Br1)

# 桥跨布置
md.spans.add(align=m1k, bridge=Br1, station=16410, ang_deg=90)  # 增加单点
md.spans.read_csv("00-MainLine/SEC201.csv")

aa = md.spans[0]

# 桥梁实例化


# 标准结构实例化
C1 = OneColumnPier(section="4*1.6", chamfer=0.5)

# C2 = std_Piers.TwoColumnsPier(section='1.6*1.6', cc=6)
# C1 = std_Piers.OneColumnPier(section='4*1.6', cham=True)
# F1=std_Foundations.KJ(section='10*8')
# BE01 = std_Beams.PercastBoxBeam()
# A1 = std_Abutments.FortAbutment()
# J1 = std_Joint.Module(v=80)
# Bearing1 = std_Bearing.Rubber(section='500*600', F4=False)
# Bearing2 = std_Bearing.Rubber(section='500*600', F4=True)
#

# 配置结构

md.spans[0].pier = C1

# for s in md.spans:
#    if s == 0:
#        s.sub_str.set(A1)
#    elif s == len(md.spans) - 1:
#        s.sub_str.set(A1, is_start=False)
#    else:
#        s.sub_str.set(C2)
#    s.found.set(F1)
#    s.sup_str.set(BE01)
#
# s.sub_str[8]=C1
##...
#
## 指定伸缩缝位置
# md.spans['10300'].ej.set(J1)
#
## 指定支座类型
# for be in md.spans.sup_str:
#    if be.st_span.ej:
#        be.st_bearing.set(Bearing2)
#    else:
#        be.st_bearing.set(Bearing1)
#    if be.ed_span.ej:
#        be.ed_span.set(Bearing2)
#    else:
#        be.ed_span.set(Bearing1)
#
md.save_srb("bin/TestProject")
