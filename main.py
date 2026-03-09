import cv2
import json
import os
import time

from video.video_source import get_video_capture
from detection.detector import detect_vehicles
from slots.slot_logic import initialize_slots, check_slots
from publisher import publish_slot_status   # NEW


# Load slots
base_dir = os.path.dirname(os.path.abspath(__file__))
slots_path = os.path.join(base_dir, "config", "slots.json")

with open(slots_path, "r") as f:
    slots = json.load(f)


# initialize slot memory
initialize_slots(len(slots))


cap = get_video_capture()

# NEW: control backend update rate
last_publish_time = 0
PUBLISH_INTERVAL = 2   # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    car_boxes = detect_vehicles(frame)
    occupied = check_slots(car_boxes, slots)

    # NEW: publish slot state periodically
    current_time = time.time()
    if current_time - last_publish_time > PUBLISH_INTERVAL:
        publish_slot_status(occupied)
        last_publish_time = current_time


    # Draw car detections
    for (x1, y1, x2, y2) in car_boxes:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Draw slots
    for i, slot in enumerate(slots):
        x, y, w, h = slot["x"], slot["y"], slot["w"], slot["h"]
        color = (0, 0, 255) if occupied[i] else (0, 255, 0)
        label = f"Slot {i+1}: {'Occupied' if occupied[i] else 'Free'}"

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    free_count = occupied.count(False)
    cv2.putText(frame, f"Free Slots: {free_count}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 255), 2)

    cv2.imshow("Smart Parking System", frame)

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()