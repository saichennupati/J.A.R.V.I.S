import pyttsx3
import pyautogui
import psutil
import pyjokes
import speech_recognition as sr
import json
import requests
import geocoder
from difflib import get_close_matches


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
g = geocoder.ip('me')
try:
    data = json.load(open('data.json'))
except Exception as e:
    print(f"Error loading data.json: {e}")
    data = {}  # default empty dict

def speak(audio) -> None:
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")
        print(audio)  # fallback to print

def screenshot() -> None:
    img = pyautogui.screenshot()
    img.save('path of folder you want to save/screenshot.png')

def cpu() -> None:
    usage = str(psutil.cpu_percent())
    print("CPU is at " + usage + " percent")

    battery = psutil.sensors_battery()
    if battery:
        print("Battery is at " + str(battery.percent) + " percent")
    else:
        print("No battery detected")

def joke() -> None:
    for i in range(5):
        speak(pyjokes.get_jokes()[i])

def takeCommand() -> str:
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Listening...')
            r.pause_threshold = 1
            r.energy_threshold = 494
            r.adjust_for_ambient_noise(source, duration=1.5)
            audio = r.listen(source)

        try:
            print('Recognizing..')
            query = r.recognize_google(audio, language='en-in')
            print(f'User said: {query}\n')

        except Exception as e:
            # print(e)

            print('Say that again please...')
            return 'None'
        return query
    except Exception as e:
        print(f"Microphone error: {e}")
        return 'None'

def weather():
    try:
        if not g or not g.latlng:
            speak("Unable to determine location for weather.")
            return
        api_url = "https://fcc-weather-api.glitch.me/api/current?lat=" + \
            str(g.latlng[0]) + "&lon=" + str(g.latlng[1])

        data = requests.get(api_url)
        data_json = data.json()
        if data_json['cod'] == 200:
            main = data_json['main']
            wind = data_json['wind']
            weather_desc = data_json['weather'][0]
            speak(str(data_json['coord']['lat']) + 'latitude' + str(data_json['coord']['lon']) + 'longitude')
            speak('Current location is ' + data_json['name'] + data_json['sys']['country'] + 'dia')
            speak('weather type ' + weather_desc['main'])
            speak('Wind speed is ' + str(wind['speed']) + ' metre per second')
            speak('Temperature: ' + str(main['temp']) + 'degree celcius')
            speak('Humidity is ' + str(main['humidity']))
        else:
            speak("Unable to fetch weather data.")
    except Exception as e:
        speak("Sorry, I couldn't retrieve the weather information.")


def translate(word):
    word = word.lower()
    if word in data:
        speak(data[word])
    elif len(get_close_matches(word, data.keys())) > 0:
        x = get_close_matches(word, data.keys())[0]
        speak('Did you mean ' + x +
              ' instead,  respond with Yes or No.')
        ans = takeCommand().lower()
        if 'yes' in ans:
            speak(data[x])
        elif 'no' in ans:
            speak("Word doesn't exist. Please make sure you spelled it correctly.")
        else:
            speak("We didn't understand your entry.")

    else:
        speak("Word doesn't exist. Please double check it.")
