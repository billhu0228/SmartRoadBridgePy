#pragma once
#include "export.h"
#include "PQXElement.h"
class IMPEXP Sprial : public PQXElement
{
private:
	double __a,__start_radius,__end_radius;
	

protected:
	double __ab__(double value, int i, int j, int k, int ll);
	static int eval_xy(double R_st, double A, double l, int idd, double* xy);
	

public:
	Sprial(void);
	Sprial(EITypeID idd, double a, double sr, double er, Vector& st, Angle& sa, LeftRightEnum direnum);


	// Í¨¹ý PQXElement ¼Ì³Ð
	//double length() const override;

	Angle end_angle() const override;

	Vector get_point_on_curve(double l_from_st) const;

};

