cmake_minimum_required(VERSION 3.16)
project(srbpy)

set(CMAKE_CXX_STANDARD 17)

# 源码统一 UTF-8，让 MSVC 按 UTF-8 解析（消除 C4819），仅 MSVC 需要
if(MSVC)
    add_compile_options(/utf-8)
endif()

# Set source directory
set(SOURCE_DIR ".")
set(ROOT "../../..")

# Tell CMake that headers are also in SOURCE_DIR
include_directories(${SOURCE_DIR})

set(SOURCES
        ${SOURCE_DIR}/binding.cpp
        ${SOURCE_DIR}/gfunc.cpp
        )

# Generate Python module (pybind11 vendored under repo lib/)
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../../lib/pybind11 pybind11_dir)
pybind11_add_module(gfunc ${SOURCES})

