//
// Created by IBD2 on 2020/10/29.
//
#include "Angle.h"
#include "Vector.h"
#include "PQX.h"
#include <pybind11\pybind11.h>
#include <pybind11\operators.h>
#include <pybind11\stl.h>

#pragma clang diagnostic push
#pragma ide diagnostic ignored "InfiniteRecursion"
namespace py = pybind11;

PYBIND11_MODULE(align_pqx, m) {
    m.def("RadToDeg", &RadToDeg);
    m.def("DegToRad", &DegToRad);
    py::class_<Angle>(m, "Angle")
            .def(py::init<>())
            .def(py::init<double>())
            .def_readonly_static("PI", &Angle::PI)
            .def("GetRadian", &Angle::GetRadian)
            .def("GetDegree", &Angle::GetDegree)
            .def("Cos", &Angle::Cos)
            .def("Sin", &Angle::Sin)
            .def(py::self * double())
            .def(py::self == py::self)
            .def(py::self + py::self);
    py::class_<Radian>(m, "Radian")
            .def(py::init<>())
            .def(py::init<double>());
    py::class_<Degree>(m, "Degree")
            .def(py::init<>())
            .def(py::init<double>());


    py::class_<Vector>(m, "Vector")
            .def(py::init<>())
            .def(py::init<double, double>())
            .def(py::init<double, double, double>())
            .def("X", &Vector::X)
            .def("Y", &Vector::Y)
            .def("Z", &Vector::Z)
            .def("length", &Vector::length)
            .def(py::self + py::self)
            .def(py::self - py::self)
            .def("__getitem__", &Vector::operator[], py::is_operator())
            .def("rotate2d", &Vector::rotate2d)
            .def("distance_point", &Vector::distance_point)
            .def("angle_signed", &Vector::angle_signed);

    py::class_<PQX>(m, "PQX")
            .def(py::init<>())
            .def(py::init<std::wstring>())
            .def_readwrite("start_pk", &PQX::start_pk)
            .def_readwrite("end_pk", &PQX::end_pk)
            .def_readwrite("start_angle", &PQX::start_angle)
            .def_readwrite("start_point", &PQX::start_point)
            .def("get_coordinate", &PQX::get_coordinate)
            .def("get_dir", &PQX::get_dir)
            .def("get_station_by_point", &PQX::get_station_by_point)
            .def("get_side", &PQX::get_side)
            .def("__binary_test__", &PQX::__binary_test__)
            .def_readonly("Text",& PQX::ICDText);

}


#pragma clang diagnostic pop