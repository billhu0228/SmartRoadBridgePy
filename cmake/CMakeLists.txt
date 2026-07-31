cmake_minimum_required(VERSION 3.16)
project(srbpy_cpp_test LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(ALIGNMENT_SOURCES
        ../src/srbpy/alignment/Angle.cpp
        ../src/srbpy/alignment/Vector.cpp
        ../src/srbpy/alignment/PQXElement.cpp
        ../src/srbpy/alignment/Straight.cpp
        ../src/srbpy/alignment/Arc.cpp
        ../src/srbpy/alignment/Sprial.cpp
        ../src/srbpy/alignment/PQX.cpp
        )

add_executable(srbpy_alignment_test
        main.cpp
        ${ALIGNMENT_SOURCES}
        )

target_include_directories(srbpy_alignment_test PRIVATE ../src/srbpy/alignment)
target_compile_definitions(
        srbpy_alignment_test
        PRIVATE SRBPY_PROJECT_ROOT="${CMAKE_CURRENT_SOURCE_DIR}/.."
        )

if(MSVC)
    target_compile_options(srbpy_alignment_test PRIVATE /utf-8)
endif()

enable_testing()
add_test(NAME alignment_cpp_smoke COMMAND srbpy_alignment_test)
