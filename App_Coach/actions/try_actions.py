from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions import actions as A

slots = {"app_choice": "medication_reminder", "practice_mode": False, "step_index": 0.0,
         "step_reply": None, "extra_help": False, "total_steps": None, "lesson_complete": False}

def tracker():
    return Tracker("me", dict(slots), {}, [], False, None, {}, "action_listen")

def run(action):
    d = CollectingDispatcher()
    for e in action.run(d, tracker(), {}):
        slots[e["name"]] = e["value"]
    for m in d.messages:
        print("BOT:", m["text"], "| overlay:", m["custom"])
run(A.ActionStartLesson())
run(A.ActionPresentStep())
slots["step_reply"] = "stuck"; run(A.ActionHandleReply()); run(A.ActionPresentStep())
slots["step_reply"] = "done";  run(A.ActionHandleReply()); run(A.ActionPresentStep())