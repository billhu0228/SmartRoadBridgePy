#include <math.h> 
#include "Angle.h"

const double Angle::PI = 3.141592653589793;

Angle::Angle(void)
{
    m_radian = 0;
};
Angle::Angle(double rad)
{
    m_radian = rad;
};

double Angle::GetRadian(void) const
{
    return this->m_radian;
}

double Angle::GetDegree(void) const
{
    return RadToDeg(this->m_radian);
}

bool Angle::IsEqual(const Angle& angle, double epsilon = 1e-6)
{
    return fabs(this->m_radian - angle.m_radian) < epsilon;
}



double Angle::Cos()  const
{
    return cos(m_radian);
}

double Angle::Sin() const
{
    return sin(m_radian);
}

Angle Angle::operator*(const double& b) const
{
    return Angle(m_radian * b);
}

bool Angle::operator==(const Angle& other) const
{
    return this->m_radian == other.m_radian;
}

Angle Angle::operator+(const Angle& other) const
{
    return Angle(m_radian + other.m_radian);
}

Radian::Radian(void) {};
Radian::Radian(double r) :Angle(r) {};
Degree::Degree(void) {};
Degree::Degree(double d) : Angle(DegToRad(d)) {};

double RadToDeg(double rad)
{
    return rad / Angle::PI * 180.0;
}

double DegToRad(double deg)
{
    return deg / 180.0 * Angle::PI;
}