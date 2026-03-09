import cv2
import os

def get_video_capture():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    video_path = os.path.join(base_dir, "..", "videos", "parking_video.mp4")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise RuntimeError("ERROR: Unable to open video source")

    return cap
