#include "Straight.h"

Straight::Straight(void)
{
	__length = 0;
}

Straight::Straight(double length, Vector& st, Angle& sdir, EITypeID idd, LeftRightEnum lr)
	:PQXElement(idd, st, sdir, lr)
{
	__length = length;
}


Vector Straight::get_point_on_curve(double l_from_st) const
{
	double x = l_from_st;
	double y = 0;
	Vector res = Vector(y, x).rotate2d(start_angle * -1);
	return start_point + res;
}


//
//double Straight::length() const
//{
//	return __length;
//}

Angle Straight::end_angle() const
{
	return Angle(start_angle.GetRadian());
	
}



