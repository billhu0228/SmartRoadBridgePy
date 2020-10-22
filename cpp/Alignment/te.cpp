#include<pybind11\pybind11.h>
namespace py = pybind11;

PYBIND11_MODULE(example, m) {
	m.doc() = "Test";
	m.def("foo", []() {
		return "Hello, Bill!";
	});

}