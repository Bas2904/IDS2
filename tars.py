from gtts import gTTS
import speech_recognition as sr
import re
import time
import webbrowser
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
import requests
from pygame import mixer
import urllib.request
import urllib.parse
import json
import bs4


def talk(audio):
    "speaks audio passed as argument"

    print(audio)
    for line in audio.splitlines():
        text_to_speech = gTTS(text=audio, lang="en-uk")
        text_to_speech.save("audio.mp3")
        mixer.init()
        mixer.music.load("audio.mp3")
        mixer.music.play()


def myCommand():
    "listens for commands"
    # Initialize the recognizer
    # The primary purpose of a Recognizer instance is, of course, to recognize speech.
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("TARS is Ready...")
        r.pause_threshold = 1
        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source, duration=1)
        # listens for the user's input
        audio = r.listen(source)
        print("analyzing...")

    try:
        command = r.recognize_google(audio).lower()
        print("You said: " + command + "\n")
        time.sleep(2)

    # loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print("Your last command couldn't be heard")
        command = myCommand()

    return command
    

def tars(command):
    errors = ["I don't know what you mean", "Excuse me?", "Can you repeat it please?"]
    "if statements for executing commands"

    #  weather forecast in your city (e.g. weather in London)
    # please create and use your own API it is free
    if "weather in" in command:
        city = command.split("in", 1)[1]   
        #openweathermap API
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=6149d074888b082134996aa4787a069a&units=metric'.format(city)
        response = requests.get(url)
        data = response.json()
        #print(data)
        temp = data['main']['temp']
        round_temp = int(round(temp))
        talk('It is {} degree celcius in {}'.format(round_temp, city))
        time.sleep(3)

    elif "hello" in command:
        talk("Hello! I am TARS. How can I help you?")
        time.sleep(3)
    elif "who are you" in command:
        talk("I am one of four former U.S. Marine Corps tactical robots")
        time.sleep(3)
    else:
        error = random.choice(errors)
        talk(error)
        time.sleep(3)

talk("TARS activated!")

# loop to continue executing multiple commands
while True:
    time.sleep(4)
    tars(myCommand())