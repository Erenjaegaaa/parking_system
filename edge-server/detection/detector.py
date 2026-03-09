from ultralytics import YOLO

model = YOLO("yolov8s.pt")  # better accuracy

def detect_vehicles(frame):
    results = model(frame, imgsz=960, conf=0.2)

    boxes = []
    for r in results:
        for box in r.boxes.xyxy:
            x1, y1, x2, y2 = map(int, box)
            boxes.append((x1, y1, x2, y2))

    return boxes





# from ultralytics import YOLO

# # Load YOLOv8 model once
# model = YOLO("yolov8s.pt")

# # COCO vehicle classes
# VEHICLE_CLASSES = [2, 3, 5, 7]  # car, motorcycle, bus, truck

# def detect_vehicles(frame):
#     results = model(frame, conf=0.2, classes=VEHICLE_CLASSES)

#     boxes = []

#     for r in results:
#         for box in r.boxes.xyxy:
#             x1, y1, x2, y2 = map(int, box)
#             boxes.append((x1, y1, x2, y2))

#     return boxes
