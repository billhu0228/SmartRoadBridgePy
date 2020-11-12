#pragma once

#include <iostream>

#include <pybind11/pybind11.h>

namespace py = pybind11;

std::vector<double>
intersection_seg_arc(double xc, double yc, double rr, double x0, double y0, double x1, double y1);


std::vector<double>
intersection_seg_seg(py::list st0, py::list ed0, py::list st1, py::list ed1);