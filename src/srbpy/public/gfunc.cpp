#include "gfunc.h"
#include <algorithm>
#include <boost/geometry.hpp>
#include <boost/geometry/geometries/point_xy.hpp>
#include <boost/geometry/geometries/point.hpp>
#include <boost/geometry/geometries/multi_point.hpp>
#include <boost/geometry/geometries/segment.hpp>
#include <boost/geometry/geometries/polygon.hpp>
#include <boost/geometry/geometries/multi_polygon.hpp>
#include <boost/geometry/geometries/linestring.hpp>
#include <boost/geometry/geometries/multi_linestring.hpp>
#include <boost/geometry/geometries/box.hpp>
#include <boost/geometry/geometries/ring.hpp>
#include <boost/geometry/geometries/variant.hpp>

namespace bg = boost::geometry;

typedef bg::model::d2::point_xy<double> DPoint;
typedef bg::model::segment<DPoint> DSegment;

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

std::vector<double> intersection_seg_seg(py::list st0, py::list ed0, py::list st1, py::list ed1) {
    std::vector<double> res;
    DPoint pt00(st0[0].cast<double>(), st0[1].cast<double>());
    DPoint pt01(ed0[0].cast<double>(), ed0[1].cast<double>());
    DPoint pt10(st1[0].cast<double>(), st1[1].cast<double>());
    DPoint pt11(ed1[0].cast<double>(), ed1[1].cast<double>());
    DSegment sg0(pt00, pt01);
    DSegment sg1(pt10, pt11);

    std::list<DPoint> lstPoints;

    if (bg::intersects(sg0, sg1)) {
        bg::intersection(sg0, sg1, lstPoints);
        res.push_back(lstPoints.begin()->x());
        res.push_back(lstPoints.begin()->y());
    }
    return res;
}

