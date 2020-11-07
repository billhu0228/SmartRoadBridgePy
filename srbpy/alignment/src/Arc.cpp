#include "Arc.h"

Arc::Arc(double r, double l, Vector& st, Angle& sdir, LeftRightEnum direnum, EITypeID idd)
	:PQXElement(idd,st,sdir,direnum)
{
	__length = l;
	__radius = r;
}

double Arc::radius(void) const
{
	return __radius;
}

//double Arc::length() const
//{
//	return __length;
//}

Angle Arc::end_angle() const
{
	return start_angle + Angle(__length / __radius) * (int)left_right;
}

Vector Arc::get_point_on_curve(double l_from_st) const
{
	double rad = l_from_st / __radius;
	double x = __radius * sin(rad);
	double y = (int)left_right * __radius * (1 - cos(rad));
	Vector res = Vector(y, x).rotate2d(start_angle * -1);
	return start_point + res;
}


