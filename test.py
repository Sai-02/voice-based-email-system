import speech_recognition as sr
import pyttsx3


def speakText(command):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(command)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=1)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2, language='en-IN')
            print(MyText)
            return MyText
    except:
        return "Sorry didn't hear what you said ??"
