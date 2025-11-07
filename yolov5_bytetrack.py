import cv2
import time
import ctypes

# 加载依赖库
ctypes.CDLL("./yolov5_trt_plugin/libyolo_plugin.so", mode=ctypes.RTLD_GLOBAL)
ctypes.CDLL("./yolov5_trt_plugin/libyolo_utils.so", mode=ctypes.RTLD_GLOBAL)
ctypes.CDLL("./build/libbytetrack.so", mode=ctypes.RTLD_GLOBAL)

# 导入YOLOv5检测器和ByteTrack跟踪器
from yolov5_trt_plugin import yolov5_trt
from build import bytetrack_trt

def draw_image(image, detections, tracks, fps):
    for track in tracks:
        x, y, w, h = track.tlwh
        track_id = track.track_id
        class_id = track.label
        x1, y1, x2, y2 = int(x), int(y), int(x+w), int(y+h)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"C:{class_id} T:{track_id}", (x1, y1 - 10), 
                   cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255), 2)
    
    cv2.putText(image, f"FPS: {fps:.2f}", (10, 30), 
               cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
    
    return image

def main(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fps_value = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'MJPG'), fps_value, (width, height))    

    detector = yolov5_trt.YOLOv5Detector("./yolov5_trt_plugin/yolov5s.engine", width, height)
    tracker = bytetrack_trt.BYTETracker(frame_rate = fps_value, track_buffer = 30)
    
    fps_list = []
    frame_count = 0
    total_time = 0.0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        start_time = time.time()
        
        # 目标检测
        detections = detector.detect(input_image=frame, 
                                    input_w=640, input_h=640, 
                                    conf_thresh=0.45, nms_thresh=0.55)
        objects = []
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            rect = bytetrack_trt.RectFloat(x1, y1, x2-x1, y2-y1)  # x, y, width, height
            obj = bytetrack_trt.Object()
            obj.rect = rect
            obj.label = det['class_id']
            obj.prob = det['confidence']
            objects.append(obj)
            
        # 目标跟踪
        tracks = tracker.update(objects)
        
        process_time = time.time() - start_time
        current_fps = 1.0 / process_time if process_time > 0 else 0
        
        frame_count += 1
        total_time += process_time
        fps_list.append(current_fps)

        # 图像绘制
        image = draw_image(frame, detections, tracks, current_fps)
        writer.write(image)

    cap.release()
    writer.release()
    
    if frame_count > 0:
        avg_fps = frame_count / total_time if total_time > 0 else 0
        print(f"Processed {frame_count} frames")
        print(f"Average FPS: {avg_fps:.2f}")
        print(f"Min FPS: {min(fps_list):.2f}")
        print(f"Max FPS: {max(fps_list):.2f}")


if __name__ == "__main__":
    input_video = "./media/sample_720p.mp4"  
    output_video = "./result.avi"  
    main(input_video, output_video)