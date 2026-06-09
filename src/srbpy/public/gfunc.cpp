#include "gfunc.h"
#include <algorithm>
#include <cmath>

std::vector<double>
intersection_seg_arc(double xc, double yc, double rr, double x0, double y0, double x1, double y1) {
    double t1, t2;
    std::vector<double> res;
    double h = xc;
    double k = yc;
    double r = rr;
    double a = (x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0);
    double b = 2 * (x1 - x0) * ((x0 - h)) + 2 * (y1 - y0) * (y0 - k);
    double c = (x0 - h) * (x0 - h) + (y0 - k) * (y0 - k) - r * r;
    if (b * b - 4 * a * c < 0) {
        return res;
    } else {
        t1 = (-b + sqrt(b * b - 4 * a * c)) / (2 * a);
        t2 = (-b - sqrt(b * b - 4 * a * c)) / (2 * a);
    }
    if (t1 >= 0 && t1 <= 1) {

        res.push_back((x1 - x0) * t1 + x0);
        res.push_back((y1 - y0) * t1 + y0);
        // res[0] = (x1 - x0) * t1 + x0;
        // res[1] = (y1 - y0) * t1 + y0;
    } else if (t2 >= 0 && t2 <= 1) {
        res.push_back((x1 - x0) * t2 + x0);
        res.push_back((y1 - y0) * t2 + y0);
        // res[0] = ((x1 - x0) * t2 + x0);
        // res[1] = ((y1 - y0) * t2 + y0);
    } else {
        // 无交点
        return res;
    }
    return res;
}

//std::vector<double> intersection_seg_seg(double *&st0, double *&ed0, double *&st1, double *&ed1) {
//    std::vector<double> res;
//    DPoint pt00(st0[0],st0[1]);
//    DPoint pt01(ed0[0],ed0[1]);
//    DPoint pt10(st1[0],st1[1]);
//    DPoint pt11(ed1[0],ed1[1]);
//    DSegment sg0(pt00,pt01);
//    DSegment sg1(pt10,pt11);
//
//    std::list<DPoint> lstPoints;
//
//    if (bg::intersects(sg0, sg1)){
//        bg::intersection(sg0, sg1, lstPoints);
//        res.push_back(lstPoints.begin()->x());
//        res.push_back(lstPoints.begin()->y());
//    }
//    return res;
//}

// 求两条线段 (st0->ed0) 与 (st1->ed1) 的交点。
// 相交返回 [x, y]；不相交返回空 vector（与原 boost::intersection 行为一致）。
// 注：平行或共线（含共线重叠）一律按“无单一交点”处理，返回空 —— 这与
// boost 对共线重叠返回重叠段端点的行为不同，但符合本工程的实际用法。
std::vector<double> intersection_seg_seg(py::list st0, py::list ed0, py::list st1, py::list ed1) {
    std::vector<double> res;
    double p0x = st0[0].cast<double>(), p0y = st0[1].cast<double>();
    double p1x = ed0[0].cast<double>(), p1y = ed0[1].cast<double>();
    double p2x = st1[0].cast<double>(), p2y = st1[1].cast<double>();
    double p3x = ed1[0].cast<double>(), p3y = ed1[1].cast<double>();

    double rx = p1x - p0x, ry = p1y - p0y;   // 线段0方向
    double sx = p3x - p2x, sy = p3y - p2y;   // 线段1方向
    double denom = rx * sy - ry * sx;        // r × s

    if (std::fabs(denom) < 1e-12) {
        // 平行或共线，无单一交点
        return res;
    }

    double qpx = p2x - p0x, qpy = p2y - p0y; // (p2 - p0)
    double t = (qpx * sy - qpy * sx) / denom;
    double u = (qpx * ry - qpy * rx) / denom;

    if (t >= 0.0 && t <= 1.0 && u >= 0.0 && u <= 1.0) {
        res.push_back(p0x + t * rx);
        res.push_back(p0y + t * ry);
    }
    return res;
}

