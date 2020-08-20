from srbpy.alignment import Align

try:
    M1 = Align(path="./00-MainLine/M1K-0312")
    k = M1.get_direction(16000)
    f = M1.get_side(471192.86358215,9856203.00274423)

    print(f)
except Exception as e:
    print(e)

# -0.8626576792206331, 0.5057882249337873
# -0.862540215993735,  0.505988513499547
