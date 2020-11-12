//
// Created by BillHu on 2020/11/12.
//

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "gfunc.h"

namespace py = pybind11;

PYBIND11_MODULE(gfunc, m) {
    m.doc() = R"pbdoc(
        Global Funcs for SRBPY
        ------------------
        .. currentmodule:: gfunc
        .. autosummary::
           :toctree: _generate

            intersection_seg_seg
            intersection_seg_arc
    )pbdoc";
    m.def("intersection_seg_arc", &intersection_seg_arc, R"pbdoc(
        求线段和圆弧的交点

        Returns:
            (float,float) : 交点坐标

    )pbdoc");

    m.def("intersection_seg_seg", &intersection_seg_seg, R"pbdoc(
        求线段和线段的交点

        Returns:
            (float,float) : 交点坐标

    )pbdoc");
}