import os
import webbrowser
from datetime import datetime

import utils

COMMANDS = [
    "open google",
    "open youtube",
    "tell time",
    "search wikipedia",
    "tell joke",
    "open application",
    "weather",
    "exit",
    "quit",
]


def main():
    utils.speak("Hello, I am your voice assistant. How can I help you today?")
    print("Voice assistant is ready. Say a command or type it below.")

    while True:
        command = utils.listen_command()
        if not command:
            command = input("Command: ").strip().lower()

        if not command:
            continue

        print(f"You said: {command}")

        if "open google" in command:
            utils.open_website("https://www.google.com")
            utils.speak("Opening Google.")

        elif "open youtube" in command:
            utils.open_website("https://www.youtube.com")
            utils.speak("Opening YouTube.")

        elif "tell time" in command or "what time" in command:
            current_time = utils.get_time()
            utils.speak(f"The current time is {current_time}")

        elif "search wikipedia" in command or "wikipedia" in command:
            query = command.replace("search wikipedia", "").replace("wikipedia", "").strip()
            if not query:
                query = input("What topic should I search on Wikipedia? ").strip()
            summary = utils.search_wikipedia(query)
            utils.speak(summary)

        elif "tell joke" in command or "joke" in command:
            joke = utils.tell_joke()
            utils.speak(joke)

        elif "open application" in command or "open app" in command:
            app_name = command.replace("open application", "").replace("open app", "").strip()
            if not app_name:
                app_name = input("Which application should I open? ").strip()
            success = utils.open_application(app_name)
            if success:
                utils.speak(f"Opening {app_name}.")
            else:
                utils.speak(f"I could not open {app_name}.")

        elif "weather" in command:
            city = command.replace("weather", "").strip()
            if not city:
                city = input("Enter a city for weather lookup: ").strip()
            weather = utils.fetch_weather(city)
            utils.speak(weather)

        elif any(keyword in command for keyword in ["exit", "quit", "stop"]):
            utils.speak("Goodbye. Have a great day.")
            break

        else:
            utils.speak("I did not understand that command. Please try again.")


if __name__ == "__main__":
    main()
