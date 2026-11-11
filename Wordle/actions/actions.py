import random
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

WORD_BANK = {
    "APPLE": "a red or green fruit that grows on trees",
    "BRAVE": "showing courage and fearlessness",
    "CRANE": "a tall bird with long legs and a long neck",
    "DREAM": "a series of thoughts or images during sleep",
    "EARTH": "the planet we live on",
    "LIGHT": "the energy that lets us see",
    "MONEY": "a medium used to buy things",
    "OCEAN": "a very large body of salt water",
    "PLANT": "a living thing that grows in soil",
    "ROBOT": "a machine that can act automatically",
    "SMILE": "a happy expression on the face",
    "TABLE": "a piece of furniture with a flat top",
    "WATER": "the clear liquid that people and animals need",
    "WORLD": "the Earth and all life on it",
    "WHALE": "a very large sea mammal",
    "HOUSE": "a building where people live",
    "TRAIN": "a vehicle that runs on rails",
    "VOICE": "the sound made when a person speaks",
    "ZEBRA": "an African animal with black-and-white stripes",
}


def get_game_context(tracker: Tracker) -> Dict[Text, Any]:
    latest_message = tracker.latest_message or {}
    metadata = latest_message.get("metadata") or {}
    return metadata.get("wordle", {}) if isinstance(metadata, dict) else {}


def get_most_common_letter(word: Text) -> Text:
    counts: Dict[Text, int] = {}
    for letter in word.upper():
        if letter.isalpha():
            counts[letter] = counts.get(letter, 0) + 1

    if not counts:
        return "Doesn't have a common letter"

    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]


def get_most_common_letter_from_metadata(game_context: Dict[Text, Any]) -> Text:
    letters: Dict[Text, int] = {}
    guesses = game_context.get("guesses") or []

    for guess in guesses:
        for letter in str(guess.get("guess", "")).upper():
            if letter.isalpha():
                letters[letter] = letters.get(letter, 0) + 1

    if not letters:
        return "Doesn't have a common letter"

    return sorted(letters.items(), key=lambda item: (-item[1], item[0]))[0][0]


class ActionWordleHint(Action):
    def name(self) -> Text:
        return "wordle_hint"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        game_context = get_game_context(tracker)
        answer = tracker.get_slot("wordle_answer") or random.choice(list(WORD_BANK.keys()))

        if game_context:
            common_letter = get_most_common_letter_from_metadata(game_context)
            message = (
                f"Hint: the most common letter in your guesses is '{common_letter}'. "
                f"Try using it in your next guess."
            )
        else:
            common_letter = get_most_common_letter(answer)
            message = (
                f"Hint: the most common letter in the secret word is '{common_letter}'. "
                f"Try using it in your next guess."
            )

        dispatcher.utter_message(text=message)
        return []


class ActionWordleDefinition(Action):
    def name(self) -> Text:
        return "wordle_definition"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        game_context = get_game_context(tracker)
        answer = tracker.get_slot("wordle_answer") or random.choice(list(WORD_BANK.keys()))

        if game_context:
            guessed_words = [item.get("guess", "") for item in (game_context.get("guesses") or []) if item.get("guess")]
            if guessed_words:
                description = f"One of your recent guesses was {guessed_words[-1].upper()}, and the letter pattern is helping narrow the word down."
            else:
                description = "The game is still in its early stages, so the word is still open to many possibilities."
        else:
            description = WORD_BANK.get(answer, "a five-letter word")

        dispatcher.utter_message(text=f"Description: {description}")
        return []
