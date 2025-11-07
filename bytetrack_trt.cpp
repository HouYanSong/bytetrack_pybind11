#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <opencv2/opencv.hpp>
#include "BYTETracker.h"

namespace py = pybind11;

PYBIND11_MODULE(bytetrack_trt, m) {
    m.doc() = "BYTETRACK Tracker using TensorRT";

    py::class_<cv::Rect_<float>>(m, "RectFloat")
        .def(py::init<>())
        .def(py::init<float, float, float, float>())
        .def_readwrite("x", &cv::Rect_<float>::x)
        .def_readwrite("y", &cv::Rect_<float>::y)
        .def_readwrite("width", &cv::Rect_<float>::width)
        .def_readwrite("height", &cv::Rect_<float>::height);

    py::class_<Object>(m, "Object")
        .def(py::init<>())
        .def_readwrite("rect", &Object::rect)
        .def_readwrite("label", &Object::label)
        .def_readwrite("prob", &Object::prob);

    py::class_<STrack>(m, "STrack")
        .def(py::init<std::vector<float>, float, int>(), 
            py::arg("tlwh"), py::arg("score"), py::arg("label") = 0)
        .def_readonly("track_id", &STrack::track_id)
        .def_readonly("tlwh", &STrack::tlwh)
        .def_readonly("label", &STrack::label);

    py::class_<BYTETracker>(m, "BYTETracker")
        .def(py::init<int, int>(), py::arg("frame_rate") = 30, py::arg("track_buffer") = 30)
        .def("update", [](BYTETracker& self, const std::vector<Object>& objects) {
            return self.update(objects);
        });
}