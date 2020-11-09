cmake_minimum_required(VERSION 3.5)

project(align_pqx)
# set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR})
set(SOURCES
        src/Angle.cpp
        src/base.cpp
        src/Vector.cpp
        src/PQXElement.cpp
        src/Straight.cpp
        src/Arc.cpp
        src/Sprial.cpp
        src/PQX.cpp
        src/bind.cpp
        )
############################################################
# Setup Boost
############################################################
set(Boost_INCLUDE_DIR E:/boost_1_74_0)
set(Boost_LIBRARY_DIR E:/boost_1_74_0/stage/lib)
include_directories(${Boost_INCLUDE_DIR})
#find_package(Boost COMPONENTS algorithm REQUIRED)
#include_directories(${Boost_INCLUDE_DIR})
#link_directories(${Boost_LIBRARY_DIR})
############################################################
# Create align_pqx.pyd
############################################################
add_subdirectory(C:/pybind11 pybind11_binary_dir)
pybind11_add_module(align_pqx
        MODULE
        ${SOURCES}
        )
target_include_directories(align_pqx
        PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        )

set_target_properties(align_pqx PROPERTIES SUFFIX ".pyd")
