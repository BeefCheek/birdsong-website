import streamlit as st
import numpy as np
import requests
import streamlit as st
from audiorecorder import audiorecorder
from pydub import AudioSegment
from io import BytesIO, StringIO
from PIL import Image




st.set_page_config(
    page_title="Piaffnet",
    layout="centered",
    page_icon=":bird:")

st.title("Piaffnet :bird:")
st.write('Birdsong Classifier')

bytes_audio = None

st.markdown("### Audio Recorder")
audio = audiorecorder("Click to record", "Click to stop recording")
audiorec = audio
if len(audiorec) > 0:
    if len(audiorec) > 4000 :
        audio = audio[1000:4000]
        output_buffer = BytesIO()
        audio.export(output_buffer, format="mp3")

        # Get the bytes from the BytesIO object
        bytes_audio = output_buffer.getvalue()
    else :
        st.write('recording too short, please record at least 4 seconds.')


st.markdown('### Audio Uploader')
uploaded_file = st.file_uploader("Choose a .mp3 file", type = ['mp3'])



url_pred = 'https://apibird-zz4jm4gkda-ew.a.run.app'

if uploaded_file is not None:

    audio = AudioSegment.from_file(uploaded_file, format='mp3')
    if len(audiorec) > 4000 :
        audio = audio[1000:4000]
        output_buffer = BytesIO()
        audio.export(output_buffer, format="mp3")

        # Get the bytes from the BytesIO object
        bytes_audio = output_buffer.getvalue()
    else :
        st.write('file too short, please updload a file that is at least 4 seconds long.')

    #st.write(requests.get('http://127.0.0.1:8000/files'))
if len(audio) > 0:

    # To play audio in frontend:
    st.audio(audio.export(bitrate='320').read())

    # To save audio to a file, use pydub export method:
    #audio.export("../to_predict/to_predict.mp3", format="mp3")

if bytes_audio is not None :
    res = requests.post(url = f"{url_pred}/uploadfile_predict?", files={'file': bytes_audio})
    predict_bird = res.json()['bird']
    predict_conf = res.json()['confidence']

    if res is not None :
        spec = predict_bird.lower().replace(' ', '_').replace('-', '_')
        #url_img = f"https://storage.cloud.google.com/birdbucket_images/bird_imgs/{spec}.jpg"
        im = Image.open(f'bird_imgs/{spec}.jpg')


if st.button('bird species prediction'):
    # print is visible in the server output, not in the page
    print('button clicked!')
    if predict_conf < 0.35:
        st.write('prediction failed, confidence too low')
        print(predict_bird, predict_conf)
    elif predict_conf < 0.55:
        st.write(predict_bird)
        st.image(im, caption=predict_bird, width=800)
        print(predict_conf)
    else :
        st.write(predict_bird)
        st.image(im, caption=predict_bird)

        st.write(f"{np.round(predict_conf, 4)*100}% of confidence.")


else:
    st.write('bird species not predicted')
