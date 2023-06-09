import sys
sys.path.append(r'c:\users\dell\anaconda3\envs\stramlit\lib\site-packages')

import streamlit as st
import pyttsx3
import speech_recognition as sr
import requests
from PIL import Image, ImageDraw, ImageOps


# Text-to-Speech Function
def text_to_speech(text, voice_id, speed, volume):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.setProperty('rate', speed)
    engine.setProperty('volume', volume/10)
    engine.say(text)
    engine.runAndWait()

# Speech-to-Text Function
def speech_to_text(language):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Say something...")
        audio_text = r.listen(source)
       
        st.write("Processing...")
        try:
            text = r.recognize_google(audio_text, language=language)
            st.write(f"You said: {text}")
        except:
            st.write("Sorry, could not recognize your voice.")

 # Function to crop image in circular shape
def crop_to_circle(image):
    width, height = image.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)
    result = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    result.putalpha(mask)
    return result

# Loading and cropping the user's profile image
profile_image = Image.open("ANKUSH.jpg")
profile_image = crop_to_circle(profile_image)

# Displaying the cropped profile image
st.sidebar.image(profile_image, use_column_width=True)           

# Main Function
def main():
    st.markdown("<h1 style='text-align: center; color: purple;'>SPEAKIFY </h1>", unsafe_allow_html=True)
    st.write("Created by [Ankush Mulkar](https://www.linkedin.com/in/ankush-mulkar-ab539454/)")

    # Download video from Google Drive
    video_url = "https://drive.google.com/file/d/1pXMXqt-cXFOmyq1_Eu8r99bIEZ849M76/view?usp=sharing"
    file_id = video_url.split('/')[-2]
    dwn_url = 'https://drive.google.com/uc?id=' + file_id
    response = requests.get(dwn_url)

    with open('video.mp4', 'wb') as f:
        f.write(response.content)

    st.video(open('video.mp4', 'rb').read())

    option = st.sidebar.selectbox("Select an option", ("Text to Speech", "Speech to Text"))

    if option == "Text to Speech":
        text = st.text_input("Enter some text")

        # Language names dictionary
        lang_names = {
            "en-US": "English (US)",
            "es-ES": "Spanish (Spain)",
            "en": "English",
            "hi": "Hindi",
            "mr": "Marathi",
            "ta": "Tamil"
        }

        voice_id = st.selectbox("Select a voice", ["Male", "Female"])
        speed = st.slider("Select the speed", 20.0, 200.0, 100.0, 0.1)
        volume = st.slider("Select the volume", 0, 10, 10, 1)

        if st.button("Convert"):
            if text:
                voice_id = 1 if voice_id == "Female" else 0
                text_to_speech(text, voice_id, speed, volume)
                st.success("Conversion successful!")
            else:
                st.write("Please enter some text.")

    elif option == "Speech to Text":
        # Language names dictionary
        lang_names = {
            "en": "English",
            "hi": "Hindi",
            "mr": "Marathi",
            "ta": "Tamil",
            "es-ES":"Spanish (Spain)"
        }

        language = st.selectbox("Select a language", [lang_names[k] for k in lang_names.keys()])

        if st.button("Start Recording"):
            speech_to_text(language)

if __name__ == "__main__":
    main()
