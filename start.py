from test import speakText, listen
import speech_recognition as sr
import pyttsx3
# while (1):
if (1):
    speakText("What do you want to do")
    speakText(" 1. Read Email ")
    speakText(" 2. Send  Email ")
    # r = sr.Recognizer()
    # with sr.Microphone() as source2:
    #     r.adjust_for_ambient_noise(source2, duration=0.2)
    #     audio2 = r.listen(source2)
    #     MyText = r.recognize_google(audio2, language='en-IN')
    #     print(MyText)
    print(listen())
