#pragma once
#include "PQXElement.h"
class Arc : public PQXElement
{
private:
	double  __radius;
public:
	Arc(void) = default;
	Arc(double r, double l, Vector& st, Angle& sdir, LeftRightEnum direnum, EITypeID idd = EITypeID::Arc);
	double radius(void) const;

	// Í¨¹ý PQXElement ¼Ì³Ð
	//double length() const override;
	Angle end_angle() const ;
	Vector get_point_on_curve(double l_from_st) const;
};

