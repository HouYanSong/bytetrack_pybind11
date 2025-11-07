
![](result.gif)

### Build plugin
```bash
sudo apt update
sudo apt install ffmpeg
sudo apt install pybind11-dev
cd bytetrack_trt_pybind11
pip install pybind11
rm -fr build
cmake -S . -B build
cmake --build build
```
```bash
[ 12%] Building CXX object CMakeFiles/bytetrack.dir/bytetrack/src/BYTETracker.cpp.o
[ 25%] Building CXX object CMakeFiles/bytetrack.dir/bytetrack/src/STrack.cpp.o
[ 37%] Building CXX object CMakeFiles/bytetrack.dir/bytetrack/src/kalmanFilter.cpp.o
[ 50%] Building CXX object CMakeFiles/bytetrack.dir/bytetrack/src/lapjv.cpp.o
[ 62%] Building CXX object CMakeFiles/bytetrack.dir/bytetrack/src/utils.cpp.o
[ 75%] Linking CXX shared library libbytetrack.so
[ 75%] Built target bytetrack
[ 87%] Building CXX object CMakeFiles/bytetrack_trt.dir/bytetrack_trt.cpp.o
[100%] Linking CXX shared module bytetrack_trt.cpython-38-aarch64-linux-gnu.so
[100%] Built target bytetrack_trt
```

### Run demo
```bash
python yolov5_bytetrack.py
```
```bash
[11/07/2025-17:13:10] [I] [TRT] Loaded engine size: 8 MiB
Deserialize yoloLayer plugin: YoloLayer
[11/07/2025-17:13:12] [I] [TRT] [MemUsageChange] Init cuBLAS/cuBLASLt: CPU +536, GPU +702, now: CPU 841, GPU 3927 (MiB)
[11/07/2025-17:13:12] [I] [TRT] [MemUsageChange] Init cuDNN: CPU +83, GPU +94, now: CPU 924, GPU 4021 (MiB)
[11/07/2025-17:13:12] [I] [TRT] [MemUsageChange] TensorRT-managed allocation in engine deserialization: CPU +0, GPU +7, now: CPU 0, GPU 7 (MiB)
[11/07/2025-17:13:12] [I] [TRT] [MemUsageChange] Init cuBLAS/cuBLASLt: CPU +0, GPU +0, now: CPU 924, GPU 4021 (MiB)
[11/07/2025-17:13:12] [I] [TRT] [MemUsageChange] Init cuDNN: CPU +0, GPU +1, now: CPU 924, GPU 4022 (MiB)
[11/07/2025-17:13:12] [I] [TRT] [MemUsageChange] TensorRT-managed allocation in IExecutionContext creation: CPU +0, GPU +11, now: CPU 0, GPU 18 (MiB)
Init ByteTrack!
Processed 1442 frames
Average FPS: 83.78
Min FPS: 68.31
Max FPS: 113.35
```