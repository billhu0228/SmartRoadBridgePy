#pragma once

#include<iostream>
#include "Angle.h"
#include <math.h>

class Vector {
private:
    double _x, _y, _z;
public:
    Vector();

    Vector(double x, double y);

    Vector(double x, double y, double z);

    double X(void);

    double Y(void);

    double Z(void);

    Vector rotate2d(const Angle &a);

    double length();

    Vector operator+(const Vector &b) const;

    Vector operator-(const Vector &b) const;

    double& operator[](int i);


    double distance_point(const Vector &other) const;

    double angle_signed(const Vector &other) const;
};

