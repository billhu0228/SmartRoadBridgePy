#include "Sprial.h"
#include <set>
using namespace std;



Sprial::Sprial(void)
{
    __a = 0;
    __start_radius = 0;
    __end_radius = 0;
}

Sprial::Sprial(EITypeID idd, double a, double sr, double er, Vector& st, Angle& sa, LeftRightEnum direnum)
    :PQXElement(idd, st, sa, direnum)
{
    __a = a;
    __start_radius = sr;
    __end_radius = er;
    __length = abs(__a * __a / __start_radius - __a * __a / __end_radius);
}

//double Sprial::length() const
//{
//    return abs(__a * __a / __start_radius - __a * __a / __end_radius);
//}

double Sprial::__ab__(double value, int i, int j, int k, int ll)
{
    double rho_a = 1.0 / __start_radius;
    double rho_b = 1.0 / __end_radius;
    double const_a = rho_a;
    double const_b = (rho_b - rho_a) / (2.0 * length());
    return pow(const_a, i) * pow(const_b, j) / (double)k * pow(value, ll);
}


Angle Sprial::end_angle() const
{
    Angle ang = Angle(0.5 * __a * __a * abs(1.0 / (__start_radius * __start_radius) - 1.0 / (__end_radius * __end_radius)));
    return ang * (double)left_right + start_angle;
}

Vector Sprial::get_point_on_curve(double l_from_st) const
{
    double x0, y0;
    double *xy=new double[2];
    eval_xy(__start_radius, __a, l_from_st, (int)TypeId,xy);

    x0 = xy[0];
    y0 = xy[1];
    y0 *= (double)left_right;
    Vector res = Vector(y0, x0).rotate2d(start_angle * -1);
    return start_point + res;
}



int Sprial::eval_xy(double R_st, double A, double l, int idd, double* xy)
{
    set<int> st1 = { 3,5 }, st2 = { 4,6 };
    double x, y;
    if (st1.find(idd) != st1.end())
    {
        x = l -
            pow(l, 3) / (6 * pow(R_st, 2)) -
            pow(l, 4) / (8 * pow(A, 2) * R_st) +
            pow(l, 6) / (72 * pow(A, 2) * pow(R_st, 3)) +
            pow(l, 5) * (pow(A, 4) - 3 * pow(R_st, 4)) / (120 * pow(A, 4) * pow(R_st, 4)) +
            pow(l, 7) * (-pow(A, 4) + 45 * pow(R_st, 4)) / (5040 * pow(A, 4) * pow(R_st, 6)) -
            pow(l, 10) / (2880 * pow(A, 6) * pow(R_st, 3)) +
            pow(l, 8) * (-pow(A, 4) + 5 * pow(R_st, 4)) / (1920 * pow(A, 6) * pow(R_st, 5)) -
            pow(l, 11) / (8448 * pow(A, 8) * pow(R_st, 2)) +
            pow(l, 9) * (-2 * pow(A, 4) + pow(R_st, 4)) / (3456 * pow(A, 8) * pow(R_st, 4)) -
            pow(l, 12) / (46080 * pow(A, 10) * R_st) -
            pow(l, 13) / (599040 * pow(A, 12));

        y = pow(l, 2) / (2 * R_st) -
            pow(l, 4) / (24 * pow(R_st, 3)) +
            pow(l, 3) / (6 * pow(A, 2)) -
            pow(l, 5) / (20 * pow(A, 2) * pow(R_st, 2)) +
            pow(l, 6) * (pow(A, 4) - 15 * pow(R_st, 4)) / (720 * pow(A, 4) * pow(R_st, 5)) +
            pow(l, 8) * (-pow(A, 4) + 105 * pow(R_st, 4)) / (40320 * pow(A, 4) * pow(R_st, 7)) +
            pow(l, 7) * (pow(A, 4) - pow(R_st, 4)) / (336 * pow(A, 6) * pow(R_st, 4)) +
            pow(l, 9) * (-pow(A, 4) + 15 * pow(R_st, 4)) / (12960 * pow(A, 6) * pow(R_st, 6)) -
            pow(l, 12) / (27648 * pow(A, 8) * pow(R_st, 3)) +
            pow(l, 10) * (-2 * pow(A, 4) + 5 * pow(R_st, 4)) / (19200 * pow(A, 8) * pow(R_st, 5)) -
            pow(l, 13) / (99840 * pow(A, 10) * pow(R_st, 2)) +
            pow(l, 11) * (-10 * pow(A, 4) + 3 * pow(R_st, 4)) / (126720 * pow(A, 10) * pow(R_st, 4)) -
            pow(l, 14) / (645120 * pow(A, 12) * R_st) -
            pow(l, 15) / (9676800 * pow(A, 14));
    }
    else if (st2.find(idd) != st2.end())
    {
        x = l -
            pow(l, 3) / (6 * pow(R_st, 2)) +
            pow(l, 4) / (8 * pow(A, 2) * R_st) -
            pow(l, 6) / (72 * pow(A, 2) * pow(R_st, 3)) +
            pow(l, 5) * (pow(A, 4) - 3 * pow(R_st, 4)) / (120 * pow(A, 4) * pow(R_st, 4)) +
            pow(l, 7) * (-pow(A, 4) + 45 * pow(R_st, 4)) / (5040 * pow(A, 4) * pow(R_st, 6)) +
            pow(l, 10) / (2880 * pow(A, 6) * pow(R_st, 3)) +
            pow(l, 8) * (pow(A, 4) - 5 * pow(R_st, 4)) / (1920 * pow(A, 6) * pow(R_st, 5)) -
            pow(l, 11) / (8448 * pow(A, 8) * pow(R_st, 2)) +
            pow(l, 9) * (-2 * pow(A, 4) + pow(R_st, 4)) / (3456 * pow(A, 8) * pow(R_st, 4)) +
            pow(l, 12) / (46080 * pow(A, 10) * R_st) -
            pow(l, 13) / (599040 * pow(A, 12));
        y = pow(l, 2) / (2 * R_st) -
            pow(l, 4) / (24 * pow(R_st, 3)) -
            pow(l, 3) / (6 * pow(A, 2)) +
            pow(l, 5) / (20 * pow(A, 2) * pow(R_st, 2)) +
            pow(l, 6) * (pow(A, 4) - 15 * pow(R_st, 4)) / (720 * pow(A, 4) * pow(R_st, 5)) +
            pow(l, 8) * (-pow(A, 4) + 105 * pow(R_st, 4)) / (40320 * pow(A, 4) * pow(R_st, 7)) +
            pow(l, 7) * (-pow(A, 4) + pow(R_st, 4)) / (336 * pow(A, 6) * pow(R_st, 4)) +
            pow(l, 9) * (pow(A, 4) - 15 * pow(R_st, 4)) / (12960 * pow(A, 6) * pow(R_st, 6)) -
            pow(l, 12) / (27648 * pow(A, 8) * pow(R_st, 3)) +
            pow(l, 10) * (-2 * pow(A, 4) + 5 * pow(R_st, 4)) / (19200 * pow(A, 8) * pow(R_st, 5)) +
            pow(l, 13) / (99840 * pow(A, 10) * pow(R_st, 2)) +
            pow(l, 11) * (10 * pow(A, 4) - 3 * pow(R_st, 4)) / (126720 * pow(A, 10) * pow(R_st, 4)) -
            pow(l, 14) / (645120 * pow(A, 12) * R_st) +
            pow(l, 15) / (9676800 * pow(A, 14));
    }
    else {
        throw exception("缓和曲线类型错误.");
    }

    if (xy == NULL)
    {
        cerr << "error: null ptr @buf" << endl;
        return NULL;
    }
    xy[0] = x;
    xy[1] = y;
    return 0;
}
