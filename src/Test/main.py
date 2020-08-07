from srbpy.alignment import Align
try:
    M1=Align(path="./00-MainLine/M1K-0312")
except Exception as e:
    print(e)

k=1