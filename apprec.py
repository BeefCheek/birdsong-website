import streamlit as st
import numpy as np
import requests
import streamlit as st
from audiorecorder import audiorecorder
from pydub import AudioSegment

st.set_page_config(
    page_title="Bird Class",
    layout="centered",
    page_icon=":bird:")

st.title("Birdsong classifier :bird:")



st.title("Audio Recorder")
audio = audiorecorder("Click to record", "Click to stop recording")

st.title('Audio Uploader')
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    #bytes_data = uploaded_file.getvalue()
    audio = AudioSegment.from_file(uploaded_file)

if len(audio) > 0:
    # To play audio in frontend:
    st.audio(audio[2000:5000].export(bitrate='312').read())

    # To save audio to a file, use pydub export method:
    audio[2000:5000].export("../to_predict/to_predict.mp3", format="mp3")

    # To get audio properties, use pydub AudioSegment properties:
    #st.write(f"Frame rate: {audio.frame_rate}, Frame width: {audio.frame_width}, Duration: {audio.duration_seconds} seconds")



url = 'http://127.0.0.1:8000/predict'
path = '../to_predict/to_predict.mp3'

url_dict = f"{url}?path={path}"
predict = requests.get(url_dict)
predict_bird = predict.json()['bird']
predict_conf = predict.json()['confidence']


if st.button('bird species prediction'):
    # print is visible in the server output, not in the page
    print('button clicked!')
    if predict_conf < 0.45:
        st.write('prediction failed, confidence too low')
    else:
        st.write(predict_bird)
        st.write(f"{np.round(predict_conf, 4)*100}% of confidence.")
else:
    st.write('bird species not predicted')
