cmake_minimum_required(VERSION 3.16...4.4)

project(srbpy LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Python 3.9 COMPONENTS Interpreter Development.Module REQUIRED)
set(PYBIND11_FINDPYTHON ON)

# pybind11 is vendored so source distributions can be built without fetching
# another C++ dependency during CMake configuration.
add_subdirectory(lib/pybind11)

pybind11_add_module(
    align_pqx
    src/srbpy/alignment/Angle.cpp
    src/srbpy/alignment/Vector.cpp
    src/srbpy/alignment/PQXElement.cpp
    src/srbpy/alignment/Straight.cpp
    src/srbpy/alignment/Arc.cpp
    src/srbpy/alignment/Sprial.cpp
    src/srbpy/alignment/PQX.cpp
    src/srbpy/alignment/binding.cpp
)
target_include_directories(align_pqx PRIVATE src/srbpy/alignment)

pybind11_add_module(
    gfunc
    src/srbpy/public/binding.cpp
    src/srbpy/public/gfunc.cpp
)
target_include_directories(gfunc PRIVATE src/srbpy/public)

if(MSVC)
    target_compile_options(align_pqx PRIVATE /utf-8)
    target_compile_options(gfunc PRIVATE /utf-8)
endif()

install(
    TARGETS align_pqx
    LIBRARY DESTINATION srbpy/alignment
    RUNTIME DESTINATION srbpy/alignment
)

install(
    TARGETS gfunc
    LIBRARY DESTINATION srbpy/public
    RUNTIME DESTINATION srbpy/public
)
