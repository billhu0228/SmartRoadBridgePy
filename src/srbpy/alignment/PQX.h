#pragma once

#include "PQXElement.h"
#include "Angle.h"
#include "Vector.h"
#include <filesystem>
#include <fstream>
#include <string>
#include <vector>

class PQX {
public:
    double start_pk, end_pk;
    Angle start_angle;
    Vector start_point;

    PQX(void);

    explicit PQX(const std::filesystem::path &filepath);

    Vector get_coordinate(double pk) const;

    Vector get_dir(double, double delta = 0.1) const;

    double get_station_by_point(double x0, double y0, int step = 10, double delta = 1e-9);

    double get_station_by_point2(double x0, double y0, double x1, double y1, double delta = 1e-6);

    int get_side(double x0, double y0);

    std::string ICDText;

private:
    std::vector<PQXElement *> elem_collection;
    // 各单元起点的累计桩号边界：[start_pk, start_pk+L0, start_pk+L0+L1, ...]
    // 构造后固定，供 get_coordinate / get_dir 共用，避免每次重建。
    std::vector<double> __len_sum_up;

    void __solve_closer(const Vector &, double ret[3]);

    void __solve_coincidence(const Vector &pt0, const Vector &pt1, double ret[2]);

    double __get_end_pk() const;

    // 重建累计桩号索引（构造末尾调用一次）
    void __rebuild_index();

    // 定位 pk 落在哪个单元，返回单元下标与该单元内的局部弧长
    void locate(double pk, int &idx, double &local_l) const;

public:
    void __binary_test__(double, double, const Vector &, double, double ret[2]);

};
