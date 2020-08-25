from srbpy import Model
from srbpy.stdlib import std_Piers, std_Beams, std_Foundations, std_Abutments  # 导入自带标准结构库
from srbpy.stdlib import std_Joint, std_Bearing  # 导入支座伸缩缝
# ---------------------------------------------------------------
# 初始化环境
md=Model()
# 导入路线资源
m1k = md.load_align(path="00-MainLine/M1K-0312", name="M1K")
m2k = md.load_align(path="00-MainLine/M2K-0312", name="M2K")
m1k.set_width(width=21.6)  # 等宽桥
m2k.set_width(dxf="M1K.dxf")  # 指定边线文件

# 桥跨布置
md.span.add(align=m1k, station=10300, ang=90) #增加单点
md.span.read_csv("SEC201.csv")

# 标准结构实例化
C2 = std_Piers.TwoColumnsPier(section='1.6*1.6', cc=6)
C1 = std_Piers.OneColumnPier(section='4*1.6', cham=True)
F1=std_Foundations.KJ(section='10*8')
BE01 = std_Beams.PercastBoxBeam()
A1 = std_Abutments.FortAbutment()
J1 = std_Joint.Module(v=80)
Bearing1 = std_Bearing.Rubber(sectiong='500*600', F4=False)
Bearing2 = std_Bearing.Rubber(sectiong='500*600', F4=True)


# 配置结构
for s in md.span:
    if s == 0:
        s.sub_str.set(A1)
    elif s == len(md.span) - 1:
        s.sub_str.set(A1, is_start=False)
    else:
        s.sub_str.set(C2)
    s.found.set(F1)
    s.sup_str.set(BE01)

s.sub_str[8]=C1
#...

# 指定伸缩缝位置
md.span['10300'].ej.set(J1)

# 指定支座类型
for be in md.span.sup_str:
    if be.st_span.ej:
        be.st_bearing.set(Bearing2)
    else:
        be.st_bearing.set(Bearing1)
    if be.ed_span.ej:
        be.ed_span.set(Bearing2)
    else:
        be.ed_span.set(Bearing1)

md.save_srb("TestBridge")
