cmake_minimum_required(VERSION 3.16)
project(ctest)

set(CMAKE_CXX_STANDARD 17)

# 源码统一 UTF-8，让 MSVC 按 UTF-8 解析（消除 C4819），仅 MSVC 需要
if(MSVC)
    add_compile_options(/utf-8)
endif()


include_directories(../src/srbpy/alignment)

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

