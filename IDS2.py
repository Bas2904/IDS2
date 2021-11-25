from gtts import gTTS
import speech_recognition as sr
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time
from pygame import mixer
import sys
import logging

# Log program actions, used to debug program errors
logging.basicConfig(filename='Program.log',
                    encoding='utf-8', level=logging.DEBUG)

# Create and open data.txt in program folder, with permission write.
# Used for saving program output in a .txt file
outfile = open('data.txt', 'w')

# Create audio file. This is he bot voice output


def talk(audio):
    "speaks audio passed as argument"
    # Creates audio.mp3, and overwrites exsisting file. Plays audio.mp3 for user
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
    # The recognizer, "recognizes" speech input from end user
    r = sr.Recognizer()
    # Use the microphone for input
    with sr.Microphone() as source:
        print("I am listening...")
        outfile.write("I am listening" + "\n")
        r.pause_threshold = 1
        # wait 1 second to let the recognizer adjust audio level
        r.adjust_for_ambient_noise(source, duration=1)
        # listens for the user input
        audio = r.listen(source)
        print("analyzing...")
        outfile.write("analyzing..." + "\n")
    # Analyze user input with google speech recogniztion, and print out result
    try:
        command = r.recognize_google(audio).lower()
        print("You said: " + command + "\n")
        outfile.write("You said: " + command + "\n")
        time.sleep(2)

    # If not able to recognize speech, loops back
    except sr.UnknownValueError:
        print("Your last command couldn't be heard")
        outfile.write("Your last command couldn't be heard" + "\n")
        command = myCommand()
        outfile.write(command + "\n")

    return command


def tars(command):
    errors = ["I don't know what you mean",
              "Excuse me?", "Can you repeat it please?"]
    "if statements for executing commands"

    #  If "weather in "City name"" is input, returns degrees from city.
    # Uses Open Weather Map API to return data in JSON
    if "weather in" in command:
        city = command.split("in", 1)[1]
        # openweathermap API
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=6149d074888b082134996aa4787a069a&units=metric'.format(
            city)
        response = requests.get(url)
        data = response.json()
        temp = data['main']['temp']
        # Rounds the celcious
        round_temp = int(round(temp))
        talk('It is {} degree celcius in {}'.format(round_temp, city))
        outfile.write('It is {} degree celcius in {}'.format(
            round_temp, city) + "\n")
        time.sleep(3)

    # Else If statement that listens for keywords, and returns a matching output
    elif "hello" in command:
        talk("Hello! I am I D S 2 point O. How can I help you?")
        outfile.write("Hello! I am TARS. How can I help you?" + "\n")
        time.sleep(3)

    elif "who are you" in command:
        talk("I am one of four former U.S. Marine Corps tactical robots")
        outfile.write(
            "I am one of four former U.S. Marine Corps tactical robots" + "\n")
        time.sleep(3)

    elif "what is life" in command:
        talk("Life is a beautiful masterpiece created by aliens for fun.")
        outfile.write(
            "Life is a beautiful masterpiece created by aliens for fun." + "\n")
        time.sleep(3)

    elif "are you hungry" in command:
        talk("No. I do not eat.")
        outfile.write("No. I do not eat." + "\n")
        time.sleep(3)

    elif "what is time" in command:
        talk("A spiderweb.")
        outfile.write("A spiderweb." + "\n")
        time.sleep(3)

    elif "what is the time" in command:
        from datetime import datetime
        now = datetime.now()
        talk("%s/%s/%s %s:%s:%s" % (now.month, now.day,
             now.year, now.hour, now.minute, now.second))
        outfile.write("%s/%s/%s %s:%s:%s" % (now.month, now.day,
                      now.year, now.hour, now.minute, now.second) + "\n")
        time.sleep(3)

    # If user says "Goodbye", the program terminates. This has to be done, in order for the program to stop.
    elif "goodbye" in command:
        talk("Bye Bye")
        outfile.write("Bye Bye" + "\n")
        time.sleep(3)
        sys.exit()

    # If no result, print an error message
    else:
        error = random.choice(errors)
        talk(error)
        outfile.write(error + "\n")
        time.sleep(3)


# Start with greeting
talk("I D S Project 2 point O activated!")
outfile.write("I D S Project 2 point O activated!" + "\n")

# loop to continue executing multiple commands
while True:
    time.sleep(4)
    tars(myCommand())
