#pragma once
#include "Vector.h"
#include "Angle.h"

enum class LeftRightEnum { NoneLR = 0, Left = -1, Right = 1 };
enum class EITypeID { NoType = 0, Line = 1, Arc = 2, ZHY = 3, YHZ = 4, BigRtoSmallR = 5, SmallRtoBigR = 6 };

class IMPEXP PQXElement
{
protected:
    EITypeID TypeId;
    Vector start_point, __end_point;
    Angle start_angle, __end_angle;
    double __length;
    LeftRightEnum left_right;

public:
    PQXElement(void);
    PQXElement(EITypeID id, Vector& pt, Angle& st_angle, LeftRightEnum lr);
    virtual Angle end_angle() const;
    virtual Vector get_point_on_curve(double l_from_st) const;
    double length() const { return __length; };
    Vector end_point() const { return get_point_on_curve(__length); };
};

