import pyaudio as py
import speech_recognition as sr
import pyttsx3 as pt
import webbrowser
import subprocess

import wikipedia

def func(cmd):
    parts = cmd.lower().split()
    q=" ".join (parts[1:])

    # if "open" in cmd.lower()f 
    if parts[0]=="open":
        print("Opening application...")
        if len(parts) > 1:
            webbrowser.open(f"https://www.{q}.com")
        else:
            print("Please specify a search to open.")
  
    if parts[0]=="search":
        print("searching in web  application...")
       
        if len(parts) > 1:
            webbrowser.open(f"https://www.google.com/search?q={q}")
        else:
            print("Please specify a app  to search.")
    if parts[0]=="start":
        print("opening system in application...")
       
        if len(parts) > 1:
            subprocess.Popen(f"start {q}",shell=True)
        else:
            print("Please specify a website to search.")
    if parts[0]=="youtube":
        print("searching in youtube  application...")
        
        if len(parts) > 1:
            webbrowser.open(f"https://www.youtube.com/results?search_query={q}")
        else:
            print("Please specify a video to search.")
    if "tell" in cmd.lower():
        print("searching in web   application...")
        if len(parts) > 1:
            try:
                print("Searching Wikipedia...")
                a=wikipedia.summary(q, sentences=2)
                print(a)
                tts_engine.say(a)
                tts_engine.runAndWait()
            except wikipedia.exceptions.DisambiguationError as e:
                print("Disambiguation error. Please be more specific.")
                tts_engine.say("Disambiguation error. Please be more specific.")
                tts_engine.runAndWait()
        else:
          
            print("Please specify a query to search.")  

    if parts[0]=="new":
        print(f" creating file {q}...")
        
        if len(parts) > 1:
            with open(f"{parts[1]}.{parts[2]}", "w") as file:
                file.write("This is a new file.")
        else:
            print("Please specify a file to search.")
    if parts[0]=="read":
        print(f" reading file {q}...")
        if len(parts) < 3:
            print("Please specify a file to read.")
            tts_engine.say("Please specify a file to read.")
            tts_engine.runAndWait()
            return
        try:
            with open(f"{parts[1]}.{parts[2]}", "r") as file:
                content = file.read()
                print(content)
                tts_engine.say(content)
                tts_engine.runAndWait()
        except FileNotFoundError:
            print(f"File {parts[1]}.{parts[2]} not found.")
            tts_engine.say(f"File {parts[1]}.{parts[2]} not found.")
            tts_engine.runAndWait()
        
    

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    tts_engine = pt.init()
    tts_engine.setProperty('rate', 150)
    tts_engine.setProperty('volume', 1.0)
    ex=0

    print("Voice assistant started. Say 'Hey Chintu' to wake me up!")

    while True:
        if ex==1:
            print("Exiting...")
            break
        with mic as source:
            audio = recognizer.listen(source, phrase_time_limit=3)

        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")

            if "exit" in text.lower() :
                print("Goodbye!")
                tts_engine.say("Goodbye!")
                tts_engine.runAndWait()
                break

            if "hey chintu" in text.lower():
                print("Hello! I'm listening...")
                tts_engine.say("How can I help you?")
                tts_engine.runAndWait()

              
                while True:
                    with mic as source:
                        print("Listening for command...")
                        audio = recognizer.listen(source, phrase_time_limit=5)
                    try:
                        cmd = recognizer.recognize_google(audio)
                        print(f"Processing command: {cmd}")

                        if "stop" in cmd.lower() or "thank you" in cmd.lower():
                            ex=1
                            print("Going back to sleep mode.")
                            tts_engine.say("Okay, going back to sleep.")
                            tts_engine.runAndWait()
                            break

                        func(cmd)

                    except sr.UnknownValueError:
                        print("Sorry, I did not understand that command.")
                    except sr.RequestError as e:
                        print(f"Could not request results; {e}")

        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
