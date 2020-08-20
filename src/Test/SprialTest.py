import sympy

# sympy.init_printing()
from sympy import I, pi, oo, integrate


def get_point_on_curve(idd, aa, st_r,  l_from_st, nn=3):
    start_r = sympy.Symbol('R_st')
    a = sympy.Symbol('A')
    l = sympy.Symbol('l')
    if idd == 3 or idd == 5:
        beta = l / start_r + l ** 2 / (2 * a ** 2)
    else:
        beta = l / start_r - l ** 2 / (2 * a ** 2)
    cos_beta_term = sympy.cos(beta).series(beta, n=None)
    sin_beta_term = sympy.sin(beta).series(beta, n=None)
    dx_dl = next(cos_beta_term)
    dy_dl = next(sin_beta_term)
    for i in range(nn):
        dx_dl += next(cos_beta_term)
        dy_dl += next(sin_beta_term)
    x = integrate(dx_dl, l)
    y = integrate(dy_dl, l)
    print(idd)
    print("x=",x)
    print("y=",y)
    #x0 = x.evalf(subs={a: aa, start_r: st_r, l: l_from_st}, n=20) - x.evalf(subs={a: aa, start_r: st_r, l: 0}, n=20)
    #y0 = y.evalf(subs={a: aa, start_r: st_r, l: l_from_st}, n=20) - y.evalf(subs={a: aa, start_r: st_r, l: 0}, n=20)
    x0 = x.evalf(subs={a: aa, start_r: st_r}, n=20) - x.evalf(subs={a: aa, start_r: st_r}, n=20)
    y0 = y.evalf(subs={a: aa, start_r: st_r}, n=20) - y.evalf(subs={a: aa, start_r: st_r}, n=20)
    return x0,y0


if __name__ == "__main__":
    get_point_on_curve(3, 500.99900199501394000000, 1e39, 200)
    get_point_on_curve(4,500.99900199501394000000,1255,200)
    #(199.87305520826719763, 5.3096764093778372609)
    #(199.87305520826719763, 5.3096764093778372409)