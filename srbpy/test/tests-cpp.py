import sys
sys.path.append(r"C:\Users\BillHu\source\python\SmartRoadBridgePy\cpp\x64\Debug")
from align_pqx import PQX,Vector

m1k = PQX("C:/Users/BillHu/source/python/SmartRoadBridgePy/srbpy/test/00-MainLine/M1K-0312/M1K-0312.ICD")
print(m1k.get_dir(18645.000258927972,0.01))
