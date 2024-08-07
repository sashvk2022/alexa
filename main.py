import shutil
import datetime
import subprocess
import os
import pyaudio
import sys
import webbrowser as web
import pyjokes
import wikipedia
import pywhatkit
import pyttsx3
import speech_recognition as sr
import wolframalpha
from urllib.request import urlopen
import json

# Initialize the recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    """Make the assistant speak the given text."""
    engine.say(text)
    engine.runAndWait()

def wish_me():
    """Greet the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        talk("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        talk("Good Afternoon Sir!")
    else:
        talk("Good Evening Sir!")
    talk("I am your Assistant, Alexa. How can I help you today?")

def take_command():
    """Listen for a command from the user."""
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
            return command
    except sr.UnknownValueError:
        talk("Sorry, I did not understand that.")
        return ""
    except sr.RequestError:
        talk("Sorry, my speech service is down.")
        return ""

def get_calculation_result(query):
    """Calculate the result of a given query using WolframAlpha."""
    try:
        app_id = "YOUR_WOLFRAMALPHA_APP_ID"
        client = wolframalpha.Client(app_id)
        res = client.query(query)
        answer = next(res.results).text
        return answer
    except StopIteration:
        return "No result found"
    except Exception as e:
        return str(e)

def process_command(command):
    """Process a given voice command."""
    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('The time is ' + time)

    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        talk(info)

    elif 'how are you' in command:
        talk("I am fine, thank you. How are you, Sir?")

    elif 'fine' in command or 'good' in command:
        talk("It's good to know that you're fine.")

    elif 'date' in command:
        talk('Sorry, I have a boyfriend.')

    elif 'are you single' in command:
        talk('I am in a relationship with WiFi.')

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'open' in command:
        if 'chrome' in command:
            web.open("https://www.google.com/")
        elif 'notepad' in command:
            subprocess.Popen(["notepad.exe"])
        elif 'youtube' in command:
            web.open("https://www.youtube.com/")
        elif 'wiki' in command:
            web.open("https://wiki.bitsathy.ac.in/")
        elif 's5' in command:
            web.open("https://wiki.bitsathy.ac.in/wiki/CSE:Semester5_23-24")
        elif 'exam' in command:
            web.open("https://moodle.bitsathy.ac.in/")
        elif 'toc' in command:
            web.open("https://wiki.bitsathy.ac.in/wiki/CSE:18CS501_23-24#Lesson_Plan_and_Schedule")
        else:
            talk('Please specify what to open.')

    elif 'search' in command:
        search_query = command.replace('search', '').strip()
        url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        web.open(url)
        talk(f"Here are the search results for {search_query}")

    elif 'is love' in command:
        talk("It is the 7th sense that destroys all other senses.")

    elif 'who are you' in command:
        talk("I am your virtual assistant created by Gaurav.")

    elif 'where is' in command:
        location = command.replace('where is', '').strip()
        url = f"https://www.google.nl/maps/place/{location.replace(' ', '%20')}"
        web.open(url)
        talk(f"Showing location for {location}")

    elif 'calculate' in command:
        try:
            indx = command.lower().split().index('calculate')
            calculation_query = ' '.join(command.split()[indx + 1:])
            answer = get_calculation_result(calculation_query)
            talk(f"The answer is {answer}")
        except ValueError:
            talk("The word 'calculate' is not followed by a valid query.")
        except Exception as e:
            talk(f"An error occurred: {str(e)}")

    elif 'news' in command:
        try:
            response = urlopen('https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=YOUR_NEWS_API_KEY')
            data = json.load(response)
            talk('Here are some top news from the Times of India:')
            for i, item in enumerate(data['articles'], start=1):
                talk(f"{i}. {item['title']}")
        except Exception as e:
            talk(f"An error occurred: {str(e)}")

    elif 'stop' in command:
        talk('Goodbye!')
        sys.exit()

    else:
        talk('Please say the command again.')

def run_alexa():
    """Run the Alexa assistant."""
    wish_me()
    while True:
        command = take_command()
        if command:
            process_command(command)

if __name__ == "__main__":
    run_alexa()
