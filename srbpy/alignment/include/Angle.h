#pragma once

#include <math.h>

class Angle {
private:
    double m_radian;

public:
    static const double PI;


    Angle(void);

    Angle(double rad);

    double GetRadian(void) const;

    double GetDegree(void) const;

    bool IsEqual(const Angle &angle, double epsilon);

    double Cos(void) const;

    double Sin(void) const;

    Angle operator*(const double &b) const;

    bool operator==(const Angle &other) const;

    Angle operator+(const Angle &other) const;
};

double RadToDeg(double rad);

double DegToRad(double deg);

class Radian : public Angle {
public:
    Radian(void);

    Radian(double r);
};

class Degree : public Angle {
public:
    Degree(void);

    Degree(double d);
};


