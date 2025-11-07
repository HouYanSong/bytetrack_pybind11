cmake_minimum_required(VERSION 3.10)

project(TensorRT_bytetrack)

set(CMAKE_CUDA_STANDARD 14)
set(CMAKE_CXX_STANDARD 14)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
find_package(pybind11 REQUIRED)
find_package(TensorRT REQUIRED)
find_package(OpenCV REQUIRED)
find_package(CUDA REQUIRED)

include_directories("/usr/include/eigen3")
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(/usr/local/cuda/include)
link_directories(/usr/local/cuda/lib64)

include_directories(${PROJECT_SOURCE_DIR}/bytetrack/include)
file(GLOB_RECURSE SRCS01 ${PROJECT_SOURCE_DIR}/bytetrack/src/*.cpp)
add_library(bytetrack SHARED ${SRCS01})
target_link_libraries(bytetrack cudart nvinfer ${OpenCV_LIBS})
set_target_properties(bytetrack PROPERTIES CUDA_ARCHITECTURES "87")

pybind11_add_module(bytetrack_trt ${PROJECT_SOURCE_DIR}/bytetrack_trt.cpp)
target_link_libraries(bytetrack_trt PRIVATE bytetrack ${OpenCV_LIBS})