cmake_minimum_required(VERSION 3.5)

project(align_exe)
# set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${PROJECT_SOURCE_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${PROJECT_SOURCE_DIR})
set(SOURCES
        ../../alignment_cpp/src/Angle.cpp
        ../../alignment_cpp/src/base.cpp
        ../../alignment_cpp/src/Vector.cpp
        ../../alignment_cpp/src/PQXElement.cpp
        ../../alignment_cpp/src/Straight.cpp
        ../../alignment_cpp/src/Arc.cpp
        ../../alignment_cpp/src/Sprial.cpp
        ../../alignment_cpp/src/PQX.cpp
        main.cpp
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
# Add an executable
############################################################
add_executable(align_exe ${SOURCES})
target_include_directories(align_exe
        PUBLIC
        ../../alignment_cpp/include
        )

