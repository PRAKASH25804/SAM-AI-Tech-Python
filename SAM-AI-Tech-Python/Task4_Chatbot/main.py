import json
from datetime import datetime
from pathlib import Path

MEMORY_PATH = Path("chat_memory.json")

DEFAULT_RESPONSES = {
    "hello": "Hello there! How can I help you today?",
    "hi": "Hi! I'm ready to chat.",
    "how are you": "I'm a Python chatbot, so I feel great when I can help.",
    "what is your name": "I am your friendly chatbot built for conversation.",
    "what time is it": "Tell me the time, or ask me directly.",
    "help": "You can ask me questions, say hello, or teach me a new response using the learn command.",
}


def load_memory():
    if MEMORY_PATH.exists():
        try:
            return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_memory(memory):
    try:
        MEMORY_PATH.write_text(json.dumps(memory, indent=2), encoding="utf-8")
    except OSError:
        pass


def normalize(text: str) -> str:
    return text.strip().lower()


def get_response(user_input: str, memory: dict) -> str:
    normalized = normalize(user_input)
    if normalized in memory:
        return memory[normalized]

    for key, answer in DEFAULT_RESPONSES.items():
        if key in normalized:
            if key == "what time is it":
                return datetime.now().strftime("The current time is %I:%M %p.")
            return answer

    if "learn" in normalized:
        return "LEARN"

    if any(keyword in normalized for keyword in ["exit", "quit", "bye", "goodbye"]):
        return "Goodbye! It was nice talking to you."

    return "I am not sure how to answer that yet. You can teach me with the learn command."


def learn_response(memory: dict):
    print("Let's learn a new response.")
    trigger = input("Enter the user prompt to teach me: ").strip().lower()
    answer = input("Enter the response I should give: ").strip()
    if trigger and answer:
        memory[trigger] = answer
        save_memory(memory)
        return f"Got it. I will respond to '{trigger}' with your answer."
    return "Learning cancelled because I need both a prompt and response."


def main():
    memory = load_memory()
    print("Chatbot is ready. Type a message or enter 'learn' to teach me.")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue

        if normalize(user_input) in ["exit", "quit", "bye", "goodbye"]:
            print("Bot: Goodbye! Have a great day.")
            break

        if "learn" in normalize(user_input):
            response = learn_response(memory)
            print(f"Bot: {response}")
            continue

        response = get_response(user_input, memory)
        print(f"Bot: {response}")


if __name__ == "__main__":
    main()
