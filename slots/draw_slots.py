import cv2
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

VIDEO_PATH = os.path.join(BASE_DIR, "..", "videos", "parking_video.mp4")
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "config", "slots.json")



slots = []
points = []

def mouse_callback(event, x, y, flags, param):
    global points, slots

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))

        # When 2 points are clicked, create a slot
        if len(points) == 2:
            x1, y1 = points[0]
            x2, y2 = points[1]

            slot = {
                "x": min(x1, x2),
                "y": min(y1, y2),
                "w": abs(x2 - x1),
                "h": abs(y2 - y1)
            }

            slots.append(slot)
            points = []

            print(f"Slot added: {slot}")

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("ERROR: Could not open video file.")
    exit()

ret, frame = cap.read()

if not ret or frame is None:
    print("ERROR: Could not read frame from video.")
    exit()

cap.release()

cv2.namedWindow("Draw Parking Slots")
cv2.setMouseCallback("Draw Parking Slots", mouse_callback)

while True:
    display = frame.copy()

    # Draw saved slots
    for slot in slots:
        cv2.rectangle(
            display,
            (slot["x"], slot["y"]),
            (slot["x"] + slot["w"], slot["y"] + slot["h"]),
            (255, 0, 0),
            2
        )

    cv2.imshow("Draw Parking Slots", display)

    key = cv2.waitKey(1)

    if key == ord("s"):  # Save
        with open(OUTPUT_FILE, "w") as f:
            json.dump(slots, f, indent=4)
        print("Slots saved.")
        break

    elif key == ord("q"):
        break

cv2.destroyAllWindows()
