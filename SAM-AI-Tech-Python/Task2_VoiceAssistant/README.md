# Task 2 — Advanced Python Voice Assistant

A professional voice assistant built with Python for desktop use. The assistant listens to voice commands, opens websites and applications, searches Wikipedia, tells jokes, reports weather, and speaks results aloud.

## Features

- Open Google
- Open YouTube
- Tell time
- Search Wikipedia
- Tell jokes
- Open applications
- Weather lookup
- Voice input and audio output

## Requirements

- Python 3.8+
- `speech_recognition`
- `pyttsx3`
- `wikipedia`
- `requests`
- `PyAudio` (for microphone input)

## Install

```bash
python -m pip install --upgrade pip
python -m pip install speechrecognition pyttsx3 wikipedia requests PyAudio
```

> On Windows, if `PyAudio` fails to install, use `pip install pipwin` then `pipwin install pyaudio`.

## Run

```bash
python main.py
```

## Usage

Speak one of the supported commands or type it when prompted. Examples:

- "Open Google"
- "Search Wikipedia Python"
- "Tell me a joke"
- "Weather London"
- "Open Notepad"
- "What time is it"
