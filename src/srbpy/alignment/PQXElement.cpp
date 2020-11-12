#include "PQXElement.h"


PQXElement::PQXElement(void)
{
	TypeId = EITypeID::NoType;
	start_point = Vector();
	start_angle = Angle();
	left_right = LeftRightEnum::NoneLR;
	__length = 0;
}

PQXElement::PQXElement(EITypeID id, Vector& pt, Angle& st_angle, LeftRightEnum lr)
{
	TypeId = id;
	start_point = pt;
	start_angle = st_angle;
	left_right = lr;
	__length = 0;
}

Angle PQXElement::end_angle() const
{
	return Angle();
}

Vector PQXElement::get_point_on_curve(double l_from_st) const
{
	
	return Vector();
}

