from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from .lessons import LESSONS, log_event


def _step(tracker: Tracker):
    """Return (app, index, step_dict) for the current lesson step."""
    app = tracker.get_slot("app_choice")
    index = int(tracker.get_slot("step_index") or 0)
    return app, index, LESSONS[app]["steps"][index]
class ActionStartLesson(Action):
    def name(self) -> Text:
        return "action_start_lesson"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        app = tracker.get_slot("app_choice")
        if app not in LESSONS:
            dispatcher.utter_message(text="Sorry, I do not have a lesson for that app yet.")
            return []
        total = len(LESSONS[app]["steps"])
        log_event(tracker.sender_id, app, 0, "lesson_started")
        mode = "practice mode" if tracker.get_slot("practice_mode") else "guided mode"
        dispatcher.utter_message(
            text=f"Great. Let's learn {LESSONS[app]['title']} in {mode}. There are {total} steps. "
                 "After each step, say 'done'. Say 'again' to hear it once more, or 'stuck' if you need help.")
        return [SlotSet("step_index", 0.0), SlotSet("total_steps", float(total)),
                SlotSet("extra_help", False), SlotSet("lesson_complete", False)]
class ActionPresentStep(Action):
    def name(self) -> Text:
        return "action_present_step"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        app, index, step = _step(tracker)
        total = len(LESSONS[app]["steps"])
        practice = bool(tracker.get_slot("practice_mode"))
        stuck = bool(tracker.get_slot("extra_help"))
        if practice and not stuck:
            text = f"Step {index + 1} of {total}. Your turn! Your goal: {step['goal']}"
            payload = {}
        else:
            text = f"Step {index + 1} of {total}. {step['instruction']}"
            if stuck:
                text += f" Here is a tip: {step['tip']}"
            payload = {"highlight": step["highlight"], "step": index + 1}

        dispatcher.utter_message(text=text, json_message=payload or None)
        log_event(tracker.sender_id, app, index + 1, "step_shown_help" if stuck else "step_shown")
        return [SlotSet("extra_help", False)]
class ActionHandleReply(Action):
    def name(self) -> Text:
        return "action_handle_reply"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        app, index, _ = _step(tracker)
        total = len(LESSONS[app]["steps"])
        reply = tracker.get_slot("step_reply")
        log_event(tracker.sender_id, app, index + 1, f"reply_{reply}")
        if reply == "done":
            if index + 1 >= total:
                return [SlotSet("lesson_complete", True)]
            dispatcher.utter_message(text="Well done!")
            return [SlotSet("step_index", float(index + 1)), SlotSet("lesson_complete", False)]
        if reply == "stuck":
            return [SlotSet("extra_help", True), SlotSet("lesson_complete", False)]
        return [SlotSet("lesson_complete", False)]
class ActionFinishLesson(Action):
    def name(self) -> Text:
        return "action_finish_lesson"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        app = tracker.get_slot("app_choice")
        log_event(tracker.sender_id, app, int(tracker.get_slot("total_steps") or 0), "lesson_completed")
        extra = "" if tracker.get_slot("practice_mode") else " Want to try again without my help? Just say 'practice'."
        dispatcher.utter_message(text=f"Congratulations! You finished the {LESSONS[app]['title']} lesson.{extra}")
        return []
class ActionWhereAmI(Action):
    def name(self) -> Text:
        return "action_where_am_i"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        app = tracker.get_slot("app_choice")
        if app not in LESSONS:
            dispatcher.utter_message(text="We have not started a lesson yet.")
            return []
        index = int(tracker.get_slot("step_index") or 0)
        dispatcher.utter_message(text=f"You are on step {index + 1} of {len(LESSONS[app]['steps'])} of the {LESSONS[app]['title']} lesson.")
        return []