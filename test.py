import speech_recognition as sr
import pyttsx3


r = sr.Recognizer()


def speakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


with sr.Microphone() as source2:
    r.adjust_for_ambient_noise(source2, duration=0.2)

    audio2 = r.listen(source2)
    MyText = r.recognize_google(audio2, language='en-IN')
    if (len(MyText) > 0):
        MyText = MyText.lower()
        print("Did you say" + MyText)
        speakText(MyText)
        speakText(
            "Hi, there how are you?  Everything, is fine here. What about you !!")
