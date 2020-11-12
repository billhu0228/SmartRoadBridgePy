cmake_minimum_required(VERSION 2.8.12)
project(test_cpp)

set(ROOT "..")
set(SOURCE_DIR "${ROOT}/src/srbpy/public")
set(Boost_INCLUDE_DIR C:/Boost/include/boost-1_74)
set(PYTHON_DIR "C:/Users/BillHu/AppData/Local/Programs/Python/Python37")


include_directories(${SOURCE_DIR})
include_directories(${Boost_INCLUDE_DIR})
include_directories(
        ${PYTHON_DIR}/include
        ${ROOT}/lib/pybind11/include
)

set(SOURCES
        ${SOURCE_DIR}/gfunc.cpp
        main.cpp
        )


add_subdirectory(H:/pybind11 pybind11_dir)

link_directories(
        ${PYTHON_DIR}/libs)
# find_package(PythonLibs REQUIRED)

add_executable(test_cpp ${SOURCES})