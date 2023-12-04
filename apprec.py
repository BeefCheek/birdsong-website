import streamlit as st
import pandas as pd
import numpy as np
import datetime
import requests
from st_audiorec import st_audiorec
import streamlit as st
from audiorecorder import audiorecorder
import librosa

st.set_page_config(
    page_title="Bird Class",
    layout="centered",
    page_icon=":bird:")

st.title("Birdsong classifier :bird:")



st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio[:3000].export().read())

    # To save audio to a file, use pydub export method:
    audio[:3000].export("to_predict.mp3", format="mp3")

    # To get audio properties, use pydub AudioSegment properties:
    #st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")


url = 'https://taxifare.lewagon.ai/predict'
path = 'raw_data/predictions/to_predict.mp3'

url_dict = f"{url}?path={path}"
predict = requests.get(url_dict)


if st.button('bird species prediction'):
    # print is visible in the server output, not in the page
    print('button clicked!')
    st.write(predict)
else:
    st.write('bird species not predicted')
