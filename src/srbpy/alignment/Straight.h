#pragma once
#include "PQXElement.h"

class Straight : public PQXElement
{
public:
	Straight(void);
	Straight(double length, Vector& st, Angle& sdir, EITypeID idd = EITypeID::Line, LeftRightEnum lr = LeftRightEnum::NoneLR);

	// ͨ�� PQXElement �̳�
	//double length() const override;
	Angle end_angle() const;
	Vector get_point_on_curve(double l_from_st) const;
};

