cmake_minimum_required(VERSION 3.16)
project(ctest)

set(CMAKE_CXX_STANDARD 11)

include_directories(../src/srbpy/alignment)
set(Boost_INCLUDE_DIR C:/Boost/include/boost-1_74)
include_directories(${Boost_INCLUDE_DIR})

set(AlignCppSrc
        ../src/srbpy/alignment/Angle.cpp
        ../src/srbpy/alignment/base.cpp
        ../src/srbpy/alignment/Vector.cpp
        ../src/srbpy/alignment/PQXElement.cpp
        ../src/srbpy/alignment/Straight.cpp
        ../src/srbpy/alignment/Arc.cpp
        ../src/srbpy/alignment/Sprial.cpp
        ../src/srbpy/alignment/PQX.cpp
        )
file(GLOB PublicCppSrc ../src/srbpy/public/*.cpp)

add_executable(ctest
        main.cpp
        ${AlignCppSrc}
        )

