cmake_minimum_required(VERSION 3.10)

project(TensorRT_bytetrack)

set(CMAKE_CUDA_STANDARD 14)
set(CMAKE_CXX_STANDARD 14)

find_package(pybind11 REQUIRED)
find_package(OpenCV REQUIRED)

include_directories("/usr/include/eigen3")
include_directories(${OpenCV_INCLUDE_DIRS})

include_directories(${PROJECT_SOURCE_DIR}/bytetrack/include)
file(GLOB_RECURSE SRCS01 ${PROJECT_SOURCE_DIR}/bytetrack/src/*.cpp)
add_library(bytetrack SHARED ${SRCS01})
target_link_libraries(bytetrack ${OpenCV_LIBS})

pybind11_add_module(byte_track ${PROJECT_SOURCE_DIR}/byte_track.cpp)
target_link_libraries(byte_track PRIVATE bytetrack ${OpenCV_LIBS})