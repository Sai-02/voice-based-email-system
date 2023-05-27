import speech_recognition as sr
import pyttsx3
import streamlit as st
import Utilities


def speakText(command):
    print(command)
    engine = pyttsx3.init()
    # voice = engine.getProperty('voices')
    # engine.setProperty('voice', voice[1].id)
    engine.setProperty('rate', 150)
    engine.say(command)
    engine.runAndWait()


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


def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.75)
        with st.spinner("Listening..."):
            audio = r.listen(source)
            st.write("Transcribing...")
            try:
                text = r.recognize_google(audio, language='en-IN')
                functions = [Utilities.isResponse1, Utilities.isResponse2, Utilities.isResponse3, Utilities.isResponseFullInbox, Utilities.isResponseGoBack, Utilities.isResponseNext, Utilities.isResponseRead, Utilities.isResponseSearchByName, Utilities.isResponseSend, Utilities.isResponseStarred, Utilities.isResponseUnread, Utilities.isResponseYes]
                # for fn in functions:
                #     if fn(text):        
                #         text = fn(text)
                #         break
                st.markdown("You said: **:green["+text+"]**")
                return text
            except sr.UnknownValueError:
                st.write("Could not understand audio")
                return ""
            except sr.RequestError as e:
                st.write("Could not request results from Google Speech Recognition service; {0}".format(e))
                return ""
