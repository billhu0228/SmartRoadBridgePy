#pragma once

#include "PQXElement.h"
#include "Angle.h"
#include "Vector.h"
#include <fstream>
#include <string>
#include <vector>
#include <boost\algorithm\string.hpp>

class PQX {
public:
    double start_pk, end_pk;
    Angle start_angle;
    Vector start_point;

    PQX(void);

    PQX(std::wstring filepath);

    Vector get_coordinate(double pk) const;

    Vector get_dir(double, double delta = 1e-4) const;

    double get_station_by_point(double x0, double y0, int step = 10, double delta = 1e-9);

    double get_station_by_point2(double x0, double y0, double x1, double y1, double delta = 1e-6);

    int get_side(double x0, double y0);

    std::wstring ICDText;

private:
    std::vector<PQXElement *> elem_collection;

    void __solve_closer(const Vector &, double ret[3]);

    void __solve_coincidence(const Vector &pt0, const Vector &pt1, double ret[2]);

    double __get_end_pk() const;

public:
    void __binary_test__(double, double, const Vector &, double, double ret[2]);

};

