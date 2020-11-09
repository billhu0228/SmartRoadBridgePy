# 比较命令，速度等
from pprint import pprint

from srbpy.alignment import Align as Align
# from srbpy.alignment import Align as AlignP
import time

M1K_C = Align(r"E:/20191213-肯尼亚高架桥施工图设计(19406)/01 前方资料/EI Data/00-MainLine/M1K-0312")
#M1K_PY = AlignP(r"E:/20191213-肯尼亚高架桥施工图设计(19406)/01 前方资料/EI Data/00-MainLine/M1K-0312")

time_start = time.time()
res = []
for i in range(3000):
    res.append(M1K_C.get_coordinate(i))
time_end = time.time()
print('C++    读取%i组坐标点，总用时%.3fs.' % (len(res), time_end - time_start))

time_start = time.time()
for loc in res:
    M1K_C.get_station_by_point(loc.X(), loc.Y())
time_end = time.time()
print('C++    查询%i组坐标点，总用时%.3fs.' % (len(res), time_end - time_start))

# time_start = time.time()
# for loc in res:
#     M1K_PY.get_station_by_point(loc.X(), loc.Y())
# time_end = time.time()
# print('Python 查询%i组坐标点，总用时%.3fs.' % (len(res), time_end - time_start))