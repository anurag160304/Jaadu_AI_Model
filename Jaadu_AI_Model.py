# Import enhanced libraries
import pyttsx3
import spotipy
import datetime
from spotipy.oauth2 import SpotifyOAuth
import speech_recognition as sr
import os
import subprocess
import time
import pygetwindow as gw
import google.generativeai as genai
import json
import requests  # For API calls
import wikipedia  # For Wikipedia integration
from email.mime.text import MIMEText  # For email features
import smtplib  # For email sending
import logging  # For error logging
from threading import Timer  # For reminder system

# Configure logging
logging.basicConfig(filename='jaadu.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open("config.json", "r") as file:
    config = json.load(file)

# Configuration variables
gemini_api_key = config["GEMINI_API_KEY"]
client_id = config["SPOTIFY_CLIENT_ID"]
client_secret = config["SPOTIFY_CLIENT_SECRET"]
weather_api_key = config["OPENWEATHER_API_KEY"]
email_password = config["EMAIL_PASSWORD"]  # Use app-specific password

# AI Configuration
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Global variables
conversation_history = []  # For maintaining context
reminders = []

# Initialize components
engine = pyttsx3.init()
engine.setProperty("rate", 200)
recognizer = sr.Recognizer()

def talk(text):
    """Text-to-Speech with error handling"""
    try:
        engine.say(text)
        engine.runAndWait()
        print(f"JAADU: {text}")
    except Exception as e:
        logging.error(f"TTS Error: {str(e)}")
        print(f"TTS Error: {str(e)}")


def listen():
    """Enhanced listening with ambient noise adjustment and debugging."""
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            recognized_text = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {recognized_text}")  # Debugging: Print recognized text
            return recognized_text
        except sr.WaitTimeoutError:
            print("No speech detected.")  # Debugging: Print if no speech is detected
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio.")  # Debugging: Print if audio is unclear
            return ""
        except Exception as e:
            logging.error(f"Recognition Error: {str(e)}")
            print(f"Recognition Error: {str(e)}")  # Debugging: Print any other errors
            return ""



# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-modify-playback-state"))

# Spotify Functions
def open_spotify():
    """Open Spotify and minimize it."""
    spotify_path = r"C:\Users\anura\AppData\Local\Microsoft\WindowsApps\Spotify.exe"
    if not os.path.exists(spotify_path):
        talk("Spotify executable not found.")
        return False
    try:
        subprocess.Popen(spotify_path, shell=True)
        time.sleep(1)
        spotify_window = gw.getWindowsWithTitle("Spotify")
        if spotify_window:
            spotify_window[0].minimize()
        talk("Spotify is open and running in the background.")
        return True
    except Exception as e:
        talk("Could not open Spotify.")
        print(e)
        return False

def play_song_on_spotify(song_name):
    """Play a specific song on Spotify."""
    open_spotify()  # Open Spotify if not already open
    time.sleep(2)  # Wait for Spotify to open
    try:
        # Check for active Spotify devices
        devices = sp.devices()
        
        if not devices["devices"]:
            talk("No active devices found. Please open Spotify on a device and try again.")
            return

        # Search for the song
        print(f"Searching for song: {song_name}")
        results = sp.search(q=song_name, type="track", limit=1)
       
        if results["tracks"]["items"]:
            track_uri = results["tracks"]["items"][0]["uri"]
            track_name = results["tracks"]["items"][0]["name"]
            artist_name = results["tracks"]["items"][0]["artists"][0]["name"]
            print(f"Found track: {track_name} by {artist_name}")

            # Start playback on the first active device
            device_id = devices["devices"][0]["id"]
            
            sp.start_playback(device_id=device_id, uris=[track_uri])
            talk(f"Playing {track_name} by {artist_name} on Spotify.")
        else:
            talk("I couldn't find the song on Spotify. Please try another one.")
    except spotipy.exceptions.SpotifyException as e:
        logging.error(f"Spotify API Error: {str(e)}")
        talk("There was an issue with Spotify. Please check your account and try again.")
    except Exception as e:
        logging.error(f"General Spotify Error: {str(e)}")
        talk("Sorry, I couldn't play the song due to an error.")

def control_spotify(action):
    """Control Spotify playback."""
    try:
        if action == "next":
            sp.next_track()
            talk("Playing the next song.")
        elif action == "previous":
            sp.previous_track()
            talk("Playing the previous song.")
        elif action == "stop":
            sp.pause_playback()
            talk("Music has been stopped.")
        else:
            talk("Invalid action.")
    except Exception as e:
        talk("An error occurred while controlling Spotify.")
        print(e)

def get_time():
    """Provide the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    talk(f"The current time is {current_time}.")

def get_weather(city):
    """Get current weather using OpenWeatherMap API"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url).json()
        if response['cod'] == 200:
            temp = response['main']['temp']
            desc = response['weather'][0]['description']
            return f"Current temperature in {city} is {temp}°C with {desc}"
        return "Could not fetch weather information"
    except Exception as e:
        logging.error(f"Weather Error: {str(e)}")
        return "Error fetching weather data"

def send_email(receiver, subject, body):
    """Send emails using SMTP"""
    try:
        sender = config["EMAIL_ADDRESS"]
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()  # Enable TLS encryption
            server.login(sender, config["EMAIL_PASSWORD"])
            server.sendmail(sender, receiver, msg.as_string())
        return "Email sent successfully"
    except smtplib.SMTPAuthenticationError:
        return "Failed to authenticate. Check your email credentials."
    except smtplib.SMTPException as e:
        return f"SMTP error occurred: {str(e)}"
    except Exception as e:
        logging.error(f"Email Error: {str(e)}")
        return f"Failed to send email: {str(e)}"
    
    
def get_ai_response(query):
    """Get AI response with conversation history"""
    try:
        global conversation_history
        conversation_history.append({"role": "user", "content": query})
        response = model.generate_content("\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in conversation_history[-6:]]
        ))
        if response.text:
            conversation_history.append({"role": "assistant", "content": response.text})
            return response.text
        return "I didn't get that, please try again"
    except Exception as e:
        logging.error(f"AI Error: {str(e)}")
        return "Error processing your request"

def run_jaadu():
    """Main function with enhanced features"""
    talk("Hello Boss! How can I assist you today?")
    while True:
        command = listen()
       
        if 'play' in command:
            # Extract the song name from the command
            song = command.replace('play', '').strip()
            # Play the song on Spotify
            play_song_on_spotify(song)
        
        elif "play next song" in command or "next" in command:
            control_spotify("next")
        elif "play previous song" in command or "previous" in command:
            control_spotify("previous")
        elif "stop song" in command or "stop" in command:
            control_spotify("stop")
        
        elif 'weather' in command:
            city = command.split('in')[-1].strip()
            talk(get_weather(city))
        
        elif 'email' in command:
            talk("Who should I send it to?")
            receiver = listen().replace(' ', '') + '@gmail.com'
            print(f"Receiver: {receiver}")  # Debugging: Print the receiver's email

            talk("What's the subject?")
            subject = listen()
            print(f"Subject: {subject}")  # Debugging: Print the email subject

            talk("What's the message?")
            body = listen()
            print(f"Body: {body}")  # Debugging: Print the email body

            result = send_email(receiver, subject, body)
            talk(result)
        
        elif 'joke' in command:
            response = get_ai_response("Tell me a short funny joke")
            talk(response)
        
        elif 'wikipedia' in command:
            query = command.replace('wikipedia', '').strip()
            talk(wikipedia.summary(query, sentences=2))

        elif "time" in command:
            get_time()   

        elif 'exit' in command:
            talk("Turning off the microphone. Goodbye!")
            listening_enabled = False  # Disable listening
            break  # Exit the loop   
        
        else:
            # For all other commands, get a response from the AI model
            response = get_ai_response(command)
            talk(response)

if __name__ == "__main__":
    try:
        run_jaadu()
    finally:
        engine.stop()