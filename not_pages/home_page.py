import streamlit as st 
from streamlit_lottie import st_lottie
import requests, pretty_midi, io
import numpy as np
from scipy.io import wavfile

def load_lottie_file(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def midi_to_wav(file):
    midi_data = pretty_midi.PrettyMIDI(file)
    audio_data = midi_data.synthesize()
    audio_data = np.int16(
        audio_data /
        np.max(np.abs(audio_data)) * 32767 * 0.9
    )  # -- Normalize 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

    audio_file = io.BytesIO()
    wavfile.write(audio_file, 44100, audio_data)
    st.audio(audio_file)




def home():
    with st.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                st_lottie(load_lottie_file(
                    'https://assets2.lottiefiles.com/temp/lf20_ERpSsi.json'), key=1, height=200)

            with col2:
                #st.subheader('Neural Music Generator', anchor='center')
                st.markdown("<h1 style='text-align: center; color: gold;'>Neural Melody Generator</h1>",
                            unsafe_allow_html=True)
                st.markdown("<h4 style='text-align: center; color: gold;'>A simple tool for creating music using AI</h4>",
                            unsafe_allow_html=True)

            with col3:
                st_lottie(load_lottie_file(
                    'https://assets2.lottiefiles.com/temp/lf20_ERpSsi.json'), height=200)

    with st.container():
        st.write('---')
        col1, col2 = st.columns(2)
        with col1:
            st.header("Music Generated Entirely With AI")
            st.markdown(
                """
                <p1 style="font-size:23px;">
                This tool uses artificial neural networks to create AI generated music on the fly. The model has been trained on a variety of genres and is able to create music based on the genre. Whether you 
                are an independent game developer, a complete beginner in music or a professional composer, Nueral Generator assists you in your creative endeavour. Create compelling melodies for your projects faster then ever before by leveraging the power 
                of AI. </p1>  
                """, unsafe_allow_html=True)
        with col2:
            lottie_file = load_lottie_file(
            "https://assets10.lottiefiles.com/packages/lf20_xnhvhcux.json")
            st_lottie(lottie_file, height=400)

    with st.container():
        st.write('---')
        st.text('')
        col1, col2 = st.columns(2)
        with col1:
            st.header('How To Get Started')
            st.markdown(
                """
                <p1 style="font-size:22px;">
                You do not need to sign up if you want to use the neural generator but you do if you want to save your files. You can save your generated files in your profile and use them later should you wish.</p1> 
            
                <ol><b>
                    <li> Navgiate to the sign up sidebar</li>
                    <li> Create an account with a valid email and password</li>
                    <li> Verify your email</li>
                    <li>Head to the login page and login using your credentials</li>
                    <li>All done! You can now save your files</li>
                </ol>
                """, unsafe_allow_html=True)

        with col2:
            st.text('')
            st.text('')
            st.image('images/gen_gui.png',
                    caption='Neural Melody Generator Interface')

    st.text('')
    with st.container():
        st.write('---')
        st.header('Samples')
        st.write('Following samples were created using the neural generator')

        st.text('Classical Music Samples')
        midi_to_wav('samples/classic_sample1.midi')
        midi_to_wav('samples/classic_sample2.midi')
        st.text('Lofi Sample')
        midi_to_wav('samples/lofi_sample1.midi')
        st.text('Game Music Sample')
        midi_to_wav('samples/game_sample1.midi')