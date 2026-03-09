import json
import datetime
import os

# -------- CONFIG --------
FREE_THRESHOLD = 15   # frames to confirm a slot is empty

# -------- MEMORY --------
slot_state = []          # True = occupied, False = free
slot_empty_count = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "config", "slot_status.json")


def initialize_slots(num_slots):
    global slot_state, slot_empty_count
    slot_state = [False] * num_slots
    slot_empty_count = [0] * num_slots


def get_car_center(car_box):
    x1, y1, x2, y2 = car_box
    return (x1 + x2) // 2, (y1 + y2) // 2


def is_center_in_slot(center, slot):
    cx, cy = center
    sx, sy, sw, sh = slot["x"], slot["y"], slot["w"], slot["h"]
    return sx <= cx <= sx + sw and sy <= cy <= sy + sh


def check_slots(car_boxes, slots):
    global slot_state, slot_empty_count

    detected_in_slot = [False] * len(slots)

    # Step 1: detect cars in slots (current frame only)
    for car in car_boxes:
        center = get_car_center(car)
        for i, slot in enumerate(slots):
            if is_center_in_slot(center, slot):
                detected_in_slot[i] = True
                break   # car can belong to only one slot

    # Step 2: update slot states with LOCKING
    for i in range(len(slots)):

        if slot_state[i]:  # slot already occupied
            if detected_in_slot[i]:
                slot_empty_count[i] = 0
            else:
                slot_empty_count[i] += 1
                if slot_empty_count[i] >= FREE_THRESHOLD:
                    slot_state[i] = False
                    slot_empty_count[i] = 0

        else:  # slot currently free
            if detected_in_slot[i]:
                slot_state[i] = True
                slot_empty_count[i] = 0

    # -------- NEW: Convert to JSON structure --------

    slot_json = {}

    for i, state in enumerate(slot_state):
        slot_id = f"S{i+1}"
        slot_json[slot_id] = "occupied" if state else "free"

    output = {
        "parking_lot_id": 1,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "slots": slot_json
    }

    # Save JSON file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=4)

    return slot_state