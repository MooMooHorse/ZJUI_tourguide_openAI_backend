import pyttsx3

def speak(sentence):
    # Initialize the converter
    engine = pyttsx3.init()

    # Set properties before adding anything to speak
    engine.setProperty('rate', 150)    # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1

    # Adding things to say
    engine.say(sentence)  # Add a string
    engine.runAndWait()   # Blocks while processing all the currently queued commands

    # Stop the engine
    engine.stop()


if __name__ == '__main__':
    # Example usage:
    speak("Land the drone!")
    speak("Watch out, there is a tree coming")