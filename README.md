# Jaadu AI Assistant

Jaadu is a voice-controlled AI assistant built with Python. It integrates various APIs and libraries to provide features like Spotify control, weather updates, email sending, Wikipedia searches, and conversational AI using Google's Gemini model.

---

## Features

- **Spotify Integration**:
  - Play specific songs.
  - Control playback (next, previous, stop).
  - Automatically open and minimize Spotify.

- **Weather Updates**:
  - Get current weather for any city using OpenWeatherMap API.

- **Email Sending**:
  - Send emails via SMTP (supports Outlook/Office365).

- **Wikipedia Integration**:
  - Fetch and read summaries from Wikipedia.

- **Conversational AI**:
  - Powered by Google's Gemini model for natural language understanding and responses.

- **Text-to-Speech (TTS) and Speech Recognition**:
  - Speak responses and listen to user commands.

- **Error Logging**:
  - Logs errors to `jaadu.log` for debugging.

---

## Prerequisites

Before running Jaadu, ensure you have the following:

1. **Python 3.8 or higher**.
2. **API Keys**:
   - Gemini API Key (from Google AI Studio).
   - Spotify Client ID and Secret (from Spotify Developer Dashboard).
   - OpenWeatherMap API Key (from OpenWeatherMap).
3. **SMTP Credentials**:
   - Email address and app-specific password for sending emails.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/jaadu-ai.git
   cd jaadu-ai

   Install dependencies:

2.Install dependencies:
pip install -r requirements.txt

3.Create a config.json file in the project directory with the following structure:
{
    "GEMINI_API_KEY": "your_gemini_api_key",
    "SPOTIFY_CLIENT_ID": "your_spotify_client_id",
    "SPOTIFY_CLIENT_SECRET": "your_spotify_client_secret",
    "OPENWEATHER_API_KEY": "your_openweather_api_key",
    "EMAIL_ADDRESS": "your_email@example.com",
    "EMAIL_PASSWORD": "your_email_password"
}
4.Ensure Spotify is installed on your system and the executable path is correct in the open_spotify() function.



##Usage

1.Run the Jaadu AI Assistant:
python Jaadu_AI_Model.py
2.Interact with Jaadu using voice commands. Here are some examples:

Play Music: "Play [song name] on Spotify."

Control Spotify: "Next song," "Previous song," "Stop music."

Weather: "What's the weather in [city]?"

Email: "Send an email."

Wikipedia: "Search Wikipedia for [query]."

Time: "What's the time?"

Joke: "Tell me a joke."

Exit: "Exit."

##Configuration
Speech Recognition: Adjust microphone settings if the assistant has trouble recognizing commands.

Spotify Path: Update the spotify_path variable in the open_spotify() function if Spotify is installed in a different location.

Logging: Logs are saved in jaadu.log for debugging purposes.

##Dependencies
pyttsx3: Text-to-speech conversion.

spotipy: Spotify API integration.

speech_recognition: Speech-to-text conversion.

google.generativeai: Google Gemini AI integration.

requests: API calls for weather and other services.

wikipedia: Fetch Wikipedia summaries.

pygetwindow: Manage Spotify window.

##Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

##License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.

##Acknowledgments
Google AI for the Gemini model.

Spotify for their API.

OpenWeatherMap for weather data.

Wikipedia for their open knowledge base.
