import tkinter as tk
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes


def talk(text):
    """Speaks the given text using pyttsx3."""
    engine.say(text)
    engine.runAndWait()


def listener():
    """Creates a recognizer object and returns the recognized command."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        command = command.lower()
        if 'yasha' in command:
            command = command.replace('yasha', '')
        return command
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None


def process_voice_input():
    """Listens for voice input, processes the command, and provides responses."""
    command = listener()
    if command:
        print(command)
        execute_command(command)
    else:
        talk("Sorry, I didn't catch that.")


def execute_command(command):
    """Executes the given command based on its content."""
    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        now = datetime.datetime.now().strftime('%I:%M %p')
        print(now)
        talk('Current time is ' + now)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 5)
        print(info)
        talk(info)
    elif 'what is' in command or 'explain' in command:
        thing = command.replace('what is', '').replace('explain', '')
        info = wikipedia.summary(thing, 7)
        print(info)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'who are you' in command:
        talk('I am an AI created by Prithivi Raj and developed by Janani.')
    elif 'how are you' in command:
        talk('I am fine, boss.')
    elif 'where are you from' in command:
        talk('I am an Assistant created in Chennai.')
    elif 'what is your name' in command:
        talk('My name is Yasha.')


def start_voice_input():
    """Disables the button, processes voice input, and re-enables the button."""
    button.config(state=tk.DISABLED)
    process_voice_input()
    button.config(state=tk.NORMAL)


# Create GUI
root = tk.Tk()
root.title("Yasha")
root.geometry("400x200")

# Button
button = tk.Button(root, text="VOICE INPUT", command=start_voice_input)
button.pack(pady=10)

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Main loop
root.mainloop()
