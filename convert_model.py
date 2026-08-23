from ultralytics import YOLO

# Load a YOLOv8n PyTorch model
model = YOLO("models/yolo11m.pt")

# Export the model to NCNN format
model.export(format="ncnn", imgsz=640, half=True)  # creates 'models/yolov8n_ncnn_model'