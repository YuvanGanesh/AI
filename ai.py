import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random

# Check for PyAudio availability
try:
    import pyaudio
    pyaudio_available = True
except ImportError:
    pyaudio_available = False

# Define questions for each subject
science_questions = [
    "What is the smallest unit of life?",
    "What is the process by which plants make their own food called?",
    "What is the name of the force that pulls objects towards the earth?",
    "What is the study of the Earth and its features called?",
    "What is the name of the gas that makes up most of the Earth's atmosphere?",
    "What planet is known as the Red Planet?",
    "What is the chemical symbol for water?",
    "What is the center of an atom called?",
    "What gas do plants absorb from the atmosphere?",
    "What is the boiling point of water in degrees Celsius?"
]
science_answers = ["cell", "photosynthesis", "gravity", "geology", "nitrogen", "mars", "h2o", "nucleus", "carbon dioxide", "100"]

maths_questions = [
    "What is 2 + 2?",
    "What is the square root of 16?",
    "What is the formula for the area of a circle?",
    "What is the value of pi (π) rounded to two decimal places?",
    "What is the process of solving an equation called?",
    "What is 10 divided by 2?",
    "What is the product of 3 and 4?",
    "What is the result of 15 minus 5?",
    "What is the next prime number after 7?",
    "What is 5 factorial (5!)?"
]
maths_answers = ["4", "4", "πr²", "3.14", "solving", "5", "12", "10", "11", "120"]

social_science_questions = [
    "What is the study of human societies and their development called?",
    "What is the system of government where citizens elect representatives to make laws?",
    "What is the largest continent on Earth?",
    "What is the historical period following the Middle Ages called?",
    "What is the document that outlines the fundamental laws of a country called?",
    "Who was the first President of the United States?",
    "What is the longest river in the world?",
    "What is the capital of France?",
    "What ancient civilization built the pyramids?",
    "What year did the First World War start?"
]
social_science_answers = ["sociology", "democracy", "asia", "renaissance", "constitution", "george washington", "nile", "paris", "egyptians", "1914"]

def talk(text):
    """Speaks the given text using pyttsx3 and prints it to the GUI."""
    engine.say(text)
    engine.runAndWait()
    output_textbox.insert(tk.END, text + "\n")

def listener():
    """Creates a recognizer object and returns the recognized command."""
    if not pyaudio_available:
        talk("PyAudio is not installed. Please install it to use the voice recognition feature.")
        return None

    r = sr.Recognizer()
    with sr.Microphone() as source:
        talk("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        command = command.lower()
        if 'yasha' in command:
            command = command.replace('yasha', '')
        return command
    except sr.UnknownValueError:
        talk("Could not understand audio")
        return None
    except sr.RequestError as e:
        talk("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

def process_voice_input():
    """Listens for voice input, processes the command, and provides responses."""
    command = listener()
    if command:
        output_textbox.insert(tk.END, "You said: " + command + "\n")
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
        talk('Current time is ' + now)
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 5)
        talk(info)
    elif 'what is' in command or 'explain' in command:
        thing = command.replace('what is', '').replace('explain', '')
        info = wikipedia.summary(thing, 7)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'who are you' in command:
        talk('I am an AI created by Team Tri-Tech')
    elif 'how are you' in command:
        talk('I am fine, boss.')
    elif 'where are you from' in command:
        talk('I am an Assistant created in Chennai.')
    elif 'what is your name' in command:
        talk('My name is Yasha.')
    elif 'quiz' in command and 'science' in command:
        conduct_quiz(science_questions, science_answers)
    elif 'quiz' in command and 'maths' in command:
        conduct_quiz(maths_questions, maths_answers)
    elif 'quiz' in command and 'social science' in command:
        conduct_quiz(social_science_questions, social_science_answers)
    else:
        talk("Sorry, I didn't understand the command.")

def conduct_quiz(questions, answers):
    """Conducts a quiz with the given questions and answers."""
    score = 0
    for i in range(len(questions)):
        question = questions[i]
        talk(question)
        user_answer = listener()
        if user_answer:
            user_answer = user_answer.lower()
            if user_answer == answers[i]:
                talk("Correct!")
                score += 1
            else:
                talk("Incorrect. The answer is " + answers[i])
        else:
            talk("No answer given. The correct answer is " + answers[i])
    talk("Quiz completed. Your score is " + str(score) + " out of " + str(len(questions)))
    output_textbox.insert(tk.END, "Quiz completed. Your score is " + str(score) + " out of " + str(len(questions)) + "\n")

def start_voice_input():
    """Disables the button, processes voice input, and re-enables the button."""
    button.config(state=tk.DISABLED)
    process_voice_input()
    button.config(state=tk.NORMAL)

# Create GUI
root = tk.Tk()
root.title("Yasha - Your Personal Assistant")
root.geometry("800x600")
root.configure(bg='#121212')

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", foreground='white', background='#6200EA', font=('Helvetica', 14, 'bold'), padding=10)
style.configure("TText", background='#121212', foreground='white', font=('Helvetica', 12))

# Title Label
title_label = tk.Label(root, text="Yasha - Your Personal Assistant", font=('Helvetica', 20, 'bold'), bg='#121212', fg='#BB86FC')
title_label.pack(pady=20)

# Button
button = ttk.Button(root, text="VOICE INPUT", command=start_voice_input)
button.pack(pady=20)

# Output Textbox
output_textbox = tk.Text(root, height=15, width=80, bg='#1E1E1E', fg='white', font=('Helvetica', 12), wrap=tk.WORD)
output_textbox.pack(pady=20)

# Initialize pyttsx3 engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index to 0 for male voice
engine.setProperty('rate', 150)

# Main loop
root.mainloop()
