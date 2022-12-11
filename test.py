import speech_recognition as sr
import pyttsx3


def speakText(command):
    engine = pyttsx3.init()
    # voice = engine.getProperty('voices')
    # engine.setProperty('voice', voice[1].id)
    engine.setProperty('rate', 150)
    engine.say(command)
    engine.runAndWait()
    print(command)


def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.75)
            audio2 = r.listen(source2)
            # MyText = r.recognize_google(audio2, language='en-IN')
            # print(MyText)
            # return MyText
            return audio2
    except Exception as e:
        print(e)
        return "Sorry didn't hear what you said ??"
