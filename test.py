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

def transcribe_speech_with_repeat():
    predictedInput = transcribe_speech()
    while (not predictedInput or len(predictedInput) == 0):
        speakText("Can you please repeat")
        st.text("Can you please repeat")
        predictedInput = transcribe_speech()
    return predictedInput

def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.75)
        with st.spinner("Listening..."):
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language='en-IN')
                functions = [Utilities.isResponse1, Utilities.isResponse2, Utilities.isResponse3, Utilities.isResponseFullInbox, Utilities.isResponseGoBack, Utilities.isResponseNext, Utilities.isResponseRead, Utilities.isResponseSearchByName, Utilities.isResponseSend, Utilities.isResponseStarred, Utilities.isResponseUnread, Utilities.isResponseYes]
                # for fn in functions:
                #     if fn(text):        
                #         text = fn(text)
                #         break
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('')
                with col2:
                    st.markdown(f'<div style="margin-bottom:15px;width:100%;display:flex;justify-content:right;"><div style="padding:5px 15px 5px 15px;width:fit-content;text-align:center;background-color: #83de76;color:black;font-size:16px;border-radius:10px 10px 0px 10px"><span style="font-weight:600;">You said:</span> '+text+'</div></div>', unsafe_allow_html=True)
                return text
            except sr.UnknownValueError:
                st.write("Could not understand audio")
                return ""
            except sr.RequestError as e:
                st.write("Could not request results from Google Speech Recognition service; {0}".format(e))
                return ""

def wake_application():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.75)
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='en-IN')
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            return ""
