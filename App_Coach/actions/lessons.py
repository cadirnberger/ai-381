"""Lesson content and a tiny logger.
The apps below are FICTIONAL demo apps. Replace the text with the real steps of your own app."""
import json
import time
from pathlib import Path

LOG_FILE = Path("lesson_log.jsonl")


def log_event(sender_id, app, step, event):
    """Append one JSON line per event. Open the file later to review what happened."""
    row = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "user": sender_id,
           "app": app, "step": step, "event": event}
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
        
LESSONS = {
    "video_call": {
        "title": "FamilyCall (demo app)",
        "steps": [            {"instruction": "Find the blue 'FamilyCall' icon on your home screen and tap it once.",
             "goal": "Open the FamilyCall app.",
             "tip": "The icon is a blue circle with a white camera. If you cannot see it, swipe left on your home screen.",
             "highlight": "app_icon"},
            {"instruction": "Tap the large green 'Call' button at the bottom of the screen.",
             "goal": "Start a new call.",
             "tip": "The button is the biggest one on the screen, near your thumb.",
             "highlight": "call_button"},
            {"instruction": "Tap your daughter's photo in the contact list.",
             "goal": "Choose who to call.",
             "tip": "Contacts are shown as photos. Scroll down gently if you do not see her.",
             "highlight": "contact_photo"},
            {"instruction": "Wait for her to answer. When you see her face, say hello! To finish, tap the red 'End' button.",
             "goal": "Finish the call.",
             "tip": "The red button is at the bottom middle of the screen.",
             "highlight": "end_button"},
        ],
    },
    "medication_reminder": {
        "title": "PillTime (demo app)",
        "steps": [
            {"instruction": "Open the 'PillTime' app by tapping the orange pill icon.",
            "goal": "Open PillTime.",
            "tip": "The icon is orange with a white pill shape.",
            "highlight": "app_icon"},
            {"instruction": "Tap the large green 'Add Reminder' button.",
            "goal": "Start a new reminder.",
            "tip": "The button is at the bottom of the screen and has a plus sign.",
            "highlight": "add_reminder_button"},
                        {"instruction": "Type the name of your medicine, then tap 'Next'.",
             "goal": "Name the medicine.",
             "tip": "You can also tap the microphone on the keyboard and say the name.",
             "highlight": "medicine_name_field"},
            {"instruction": "Pick the time of day you take it, then tap the green 'Save' button.",
             "goal": "Set the time and save.",
             "tip": "Tap the clock face, move the hands, and press 'OK'. Then press Save.",
             "highlight": "save_button"},
        ],
    },
}