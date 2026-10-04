import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
import pyttsx3
import ollama
from datetime import datetime


# ==============================
# TEXT TO SPEECH
# ==============================

engine = pyttsx3.init()


def speak(text):
    print("Assistant:", text)

    engine.say(text)
    engine.runAndWait()


# ==============================
# AI FUNCTION - LLAMA 3.2
# ==============================

def ask_ai(question):

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response["message"]["content"]


# ==============================
# RECORDING SETTINGS
# ==============================

duration = 5
sample_rate = 44100


# ==============================
# SPEECH RECOGNITION
# ==============================

recognizer = sr.Recognizer()


# ==============================
# COMMAND PROCESSING
# ==============================

def process_command(command):

    command = command.lower().strip()

    # ------------------------------
    # Hello
    # ------------------------------

    if command in ["hello", "hi", "hey"]:

        return "Hello! How can I help you?"


    # ------------------------------
    # Time
    # ------------------------------

    elif "time" in command:

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}"


    # ------------------------------
    # Date
    # ------------------------------

    elif "date" in command:

        current_date = datetime.now().strftime("%d %B %Y")

        return f"Today's date is {current_date}"


    # ------------------------------
    # Python
    # ------------------------------

    elif "what is python" in command:

        return (
            "Python is a high-level programming language "
            "used for web development, automation, data analysis "
            "and artificial intelligence."
        )


    # ------------------------------
    # Django
    # ------------------------------

    elif "what is django" in command:

        return (
            "Django is a Python web framework used to build "
            "secure and scalable web applications."
        )


    # ------------------------------
    # Who are you
    # ------------------------------

    elif "who are you" in command:

        return "I am your Python Voice Virtual Assistant."


    # ------------------------------
    # Exit
    # ------------------------------

    elif (
        "bye" in command
        or "exit" in command
        or "stop" in command
    ):

        return "Goodbye!"


    # ------------------------------
    # AI - Llama 3.2
    # ------------------------------

    else:

        return ask_ai(command)


# ==============================
# START ASSISTANT
# ==============================

print("===================================")
print("     VOICE VIRTUAL ASSISTANT")
print("===================================")

print("Voice Assistant started!")
print("Say 'bye' to exit.")


# ==============================
# MAIN LOOP
# ==============================

while True:

    # ------------------------------
    # RECORD VOICE
    # ------------------------------

    print("\nSpeak now...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32"
    )

    sd.wait()


    # ------------------------------
    # SAVE AUDIO
    # ------------------------------

    sf.write(
        "voice.wav",
        recording,
        sample_rate
    )

    print("Recording finished.")


    # ------------------------------
    # CONVERT VOICE TO TEXT
    # ------------------------------

    with sr.AudioFile("voice.wav") as source:

        print("Processing your voice...")

        audio = recognizer.record(source)


    # ------------------------------
    # SPEECH TO TEXT
    # ------------------------------

    try:

        text = recognizer.recognize_google(audio)

        print("You said:", text)


        # ------------------------------
        # PROCESS COMMAND
        # ------------------------------

        response = process_command(text)


        # ------------------------------
        # SPEAK RESPONSE
        # ------------------------------

        speak(response)


        # ------------------------------
        # EXIT
        # ------------------------------

        command = text.lower().strip()

        if (
            "bye" in command
            or "exit" in command
            or "stop" in command
        ):

            break


    except sr.UnknownValueError:

        print(
            "Sorry, I could not understand the audio."
        )


    except sr.RequestError as error:

        print(
            "Speech service error:",
            error
        )


    except Exception as error:

        print(
            "Error:",
            error
        )