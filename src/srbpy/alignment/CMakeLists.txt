cmake_minimum_required(VERSION 2.8.12)
project(srbpy)

# Set include directories

# Set source directory
set(SOURCE_DIR ".")
set(ROOT "../../..")

# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})

set(Boost_INCLUDE_DIR C:/Boost/include/boost-1_74)
include_directories(${Boost_INCLUDE_DIR})

set(SOURCES
    ${SOURCE_DIR}/Angle.cpp
    ${SOURCE_DIR}/base.cpp
    ${SOURCE_DIR}/Vector.cpp
    ${SOURCE_DIR}/PQXElement.cpp
    ${SOURCE_DIR}/Straight.cpp
    ${SOURCE_DIR}/Arc.cpp
    ${SOURCE_DIR}/Sprial.cpp
    ${SOURCE_DIR}/PQX.cpp
    ${SOURCE_DIR}/binding.cpp
    )

# Generate Python module
add_subdirectory(${ROOT}/lib/pybind11 pybind11_dir)
pybind11_add_module(align_pqx ${SOURCES})

find_package(PythonLibs REQUIRED)

include_directories(
    ${PYTHON_INCLUDE_DIRS}
    lib
    lib/pybind11/include
)

