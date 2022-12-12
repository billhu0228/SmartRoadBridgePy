#include "Vector.h"


Vector::Vector() {
    _x = 0;
    _y = 0;
    _z = 0.0;
}

Vector::Vector(double x, double y) {
    _x = x;
    _y = y;
    _z = 0.0;
}

Vector::Vector(double x, double y, double z) {
    _x = x;
    _y = y;
    _z = z;
}

double Vector::X() const {
    return _x;
}

double Vector::Y(void) const {
    return _y;
}

double Vector::Z(void) const {
    return _z;
}

Vector Vector::rotate2d(const Angle &a) {
    double x = _x * a.Cos() - _y * a.Sin();
    double y = _x * a.Sin() + _y * a.Cos();
    return Vector(x, y, _z);
}

double Vector::length() {
    return sqrt(_x * _x + _y * _y + _z * _z);
}

Vector Vector::operator+(const Vector &b) const {
    return Vector(_x + b._x, _y + b._y, _z + b._z);
}

Vector Vector::operator-(const Vector &b) const {
    return Vector(_x - b._x, _y - b._y, _z - b._z);
}

double Vector::distance_point(const Vector &other) const {
    return ((*this) - other).length();
}

/// 返回带符号的夹角，值域为(-pi,pi],调用了atan2函数.
/// \param other
/// \return
double Vector::angle_signed(const Vector &other) const {
    if (_z != 0 || other._z != 0) {
        throw std::exception("读取ICD文件错误.");
    }
    double dot = _x * other._x + _y * other._y;
    double det = _x * other._y - _y * other._x;
    double ret = atan2(det, dot);
    return ret;
}


double &Vector::operator[](int i) {
    if (i == 0) { return _x; }
    else if (i == 1) { return _y; }
    else if (i == 2) { return _z; }
    else { throw std::exception("%d 超过索引长度.", i); }

}