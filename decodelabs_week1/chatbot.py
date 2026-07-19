"""
Project 1: Rule-Based AI Chatbot (Enhanced Version)
DecodeLabs - Industrial Training Kit (Batch 2026)

Improvements over v1:
  - Bigger vocabulary (multiple phrasings per intent)
  - Keyword-based matching (not just exact match) via nested logic
  - Simple personality + name memory (state)
  - Randomized replies so it doesn't feel robotic
  - Cleaner "IPO" structure: Input -> Process -> Output
"""

import random
import re

# ---------------------------------------------------------
# KNOWLEDGE BASE: each intent maps to a list of possible
# trigger keywords AND a list of possible responses.
# ---------------------------------------------------------
KNOWLEDGE_BASE = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "yo", "good morning", "good evening"],
        "responses": [
            "Hey there! 👋",
            "Hello! Great to see you.",
            "Hi! What's on your mind?",
        ],
    },
    "wellbeing": {
        "keywords": ["how are you", "how's it going", "how do you do"],
        "responses": [
            "I'm just a bunch of if-else logic, but I'm running great!",
            "All systems green. Thanks for asking!",
        ],
    },
    "identity": {
        "keywords": ["your name", "who are you"],
        "responses": [
            "I'm RuleBot, DecodeLabs' Project 1 chatbot.",
            "Call me RuleBot — built on pure logic, no ML yet!",
        ],
    },
    "capability": {
        "keywords": ["what can you do", "help", "commands"],
        "responses": [
            "I can greet you, tell you my name, remember yours, and chat a bit. Type 'bye' to leave.",
        ],
    },
    "gratitude": {
        "keywords": ["thank you", "thanks", "appreciate"],
        "responses": [
            "You're welcome!",
            "Anytime! 😊",
        ],
    },
    "mood_good": {
        "keywords": ["i am fine", "i'm good", "doing well", "i'm great"],
        "responses": [
            "Glad to hear that!",
            "That's awesome!",
        ],
    },
    "mood_bad": {
        "keywords": ["i am sad", "not good", "feeling down", "i'm tired"],
        "responses": [
            "Sorry to hear that. Take it easy on yourself.",
            "Hope things get better soon.",
        ],
    },
}

EXIT_COMMANDS = {"bye", "exit", "quit", "goodbye", "see you"}
FALLBACK_RESPONSES = [
    "I do not understand. Try typing 'help' to see what I can do.",
    "Hmm, that's outside my rules for now. Try asking my name or saying hello!",
]

# Simple state (memory) — kept minimal on purpose for a rule-based bot
state = {"user_name": None}


def sanitize(raw_input: str) -> str:
    """Phase 1: Sanitization & Normalization."""
    return raw_input.lower().strip()


def extract_name(clean_input: str):
    """Nested-logic example: detect 'my name is X' and remember it."""
    if "my name is" in clean_input:
        name = clean_input.split("my name is", 1)[1].strip().title()
        return name if name else None
    return None


def match_intent(clean_input: str):
    """Phase 2 (Process): keyword-based intent matching using word boundaries
    (so 'yo' doesn't accidentally match inside 'you')."""
    for intent, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"]:
            pattern = r"\b" + re.escape(keyword) + r"\b"
            if re.search(pattern, clean_input):
                return random.choice(data["responses"])
    return None


def get_response(clean_input: str) -> str:
    """Combines name-memory logic with keyword matching, falls back if nothing hits."""
    # Nested condition: name introduction takes priority
    name = extract_name(clean_input)
    if name:
        state["user_name"] = name
        return f"Nice to meet you, {name}!"

    # Personalize replies once we know the user's name
    reply = match_intent(clean_input)
    if reply:
        if state["user_name"] and random.random() < 0.4:
            reply += f" ({state['user_name']})"
        return reply

    return random.choice(FALLBACK_RESPONSES)


def run_chatbot():
    """The Heartbeat: continuous loop that keeps the bot alive until exit."""
    print("RuleBot: Hello! I'm your rule-based AI chatbot. Type 'bye' to exit.")

    while True:
        raw_input_text = input("You: ")
        clean_input = sanitize(raw_input_text)

        if clean_input in EXIT_COMMANDS:
            name = state["user_name"]
            farewell = f"Goodbye, {name}! 👋" if name else "Goodbye! 👋"
            print(f"RuleBot: {farewell}")
            break

        reply = get_response(clean_input)
        print(f"RuleBot: {reply}")


if __name__ == "__main__":
    run_chatbot()