cmake_minimum_required(VERSION 3.20)

project(bryc2)

include(${CMAKE_SOURCE_DIR}/bryc.cmake)
include(CTest)
enable_testing()
add_subdirectory(tests)