import requests
import json
from datetime import datetime
from config.settings import BACKEND_URL, PARKING_LOT_ID


def publish_slot_status(slot_state):
    """
    slot_state example:
    [True, False, True, False]
    """

    slot_json = {}

    for i, state in enumerate(slot_state):
        slot_id = f"S{i+1}"
        slot_json[slot_id] = "occupied" if state else "free"

    payload = {
        "parking_lot_id": PARKING_LOT_ID,
        "timestamp": datetime.utcnow().isoformat(),
        "slots": slot_json
    }

    try:
        response = requests.post(BACKEND_URL, json=payload)

        if response.status_code == 200:
            print("Slot update sent successfully")
        else:
            print("Backend returned error:", response.text)

    except Exception as e:
        print("Failed to send slot update:", e)