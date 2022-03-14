import requests
import webbrowser
import pyrebase
import streamlit as st
from fileinput import filename
import streamlit as st
from streamlit_lottie import st_lottie
from models.pokemon_model.pokemon_model import generate_pokemon
from models.beethoven_model.beethoven_model import generate_beethoven
from models.folk_model.folk_model import generate_folk
from models.lofi_model.lofi_model import generate_lofi
#import os
import re
import numpy as np
import pretty_midi
import io
from scipy.io import wavfile

# Page assets

def load_lottie_file(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_file = load_lottie_file("https://assets10.lottiefiles.com/packages/lf20_xnhvhcux.json")


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

# Configuration Key
firebaseConfig = {

    "apiKey": "AIzaSyDvhPa-Yyz7TUcptE8Ga_2Yiz_tK1KcPMA",
    "authDomain": "streamlit-c5243.firebaseapp.com",
    "projectId": "streamlit-c5243",
    "databaseURL": "https://streamlit-c5243-default-rtdb.europe-west1.firebasedatabase.app/",
    "storageBucket": "streamlit-c5243.appspot.com",
    "messagingSenderId": "1083626971499",
    "appId": "1:1083626971499:web:47ac2c4321b0a4840f6c2e",
    "measurementId": "G-XG4RTFPMWS"

}

st.set_page_config(page_title='Neural Music Generator',
                   page_icon=':musical_note:', layout='wide')




# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()


st.sidebar.title("Navigation Panel")


# Authentication
choice = st.sidebar.selectbox('Pages', ['Home','Login', 'Sign up'])


if choice == 'Sign up':
    email = st.sidebar.text_input(
        'Please enter your email address', placeholder='Email')
    password = st.sidebar.text_input(
        'Please enter your password', type='password', placeholder='Password')
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'    
    handle = st.sidebar.text_input(
            'Please input your app handle name', value='Default')
    submit = st.sidebar.button('Create my account')
    
    try:
        if submit:
            if email and password:
                if re.search(regex, email):
                    user = auth.create_user_with_email_and_password(
                        email, password)
                    st.success('Your account is created successfully!')
                    st.balloons()

                    # Sign in
                    user = auth.sign_in_with_email_and_password(
                        email, password)

                    # creating a tree with the name localID with two child leafs that have values
                    db.child(user["localId"]).child("Handle").set(handle)
                    # givin the name of tree branch(localid) to the name
                    db.child(user["localId"]).child("ID").set(user["localId"])
                    # the ID is the same as the Auth UIID
                    st.title(f'Welcome {handle}')
                    st.info('Login via login drop down select menu ')
                else:
                    st.warning('Invalid Email')
            else:
                st.error('Please fill email and password fields')

    except requests.HTTPError as f:
        st.error('Error! Email is already registered or Password is too weak')


if choice == 'Login':
    email = st.sidebar.text_input(
        'Please enter your email address', placeholder='Email')
    password = st.sidebar.text_input(
        'Please enter your password', type='password', placeholder='Password')
    login = st.sidebar.checkbox('Login/Logout')
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if login:
        if email and password:
            if re.search(regex, email):
                user = auth.sign_in_with_email_and_password(email, password)
                st.write(
                    '<style>div.row-widget.stRadio > div{flex-direction:row;} ', unsafe_allow_html=True)

                pages = st.radio(
                    'Jump to', ['Neural Generator', 'Upload a file', 'Generated MIDIs'])

                if pages == 'Upload a file':
                    uploaded_file = st.file_uploader('Choose a file')
                    upload = st.button('Upload')

                    if upload:
                        try:

                            uid = user['localId']
                            # fireb_upload = storage.child(uid).put(uploaded_file, user['idToken'])
                            # stored_file = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                            # db.child(uid).child('Audio_Files').push(stored_file)
                            # st.success('File successfully uploaded')
                            fireb_upload = storage.child(uploaded_file.name).put(
                                uploaded_file, user['idToken'])
                            stored_file = storage.child(uploaded_file.name).get_url(
                                fireb_upload['downloadTokens'])
                            db.child(uid).child(
                                'Audio_Files').push(stored_file)
                            st.success('File successfully uploaded')

                        except:
                            st.error('Please select a file to upload!')

                elif pages == 'Generated MIDIs':
                    Audio = db.child(user['localId']).child(
                        'Audio_Files').get()
                    file_choices = []

                    try:
                        for i in Audio.each():
                            i_choice = i.val()
                            file_choices.append(i_choice)

                        file_to_be_downloaded = st.radio(
                            'Select the file you would like to download', file_choices)
                        if st.button('Download'):
                            webbrowser.open_new_tab(file_to_be_downloaded)
                        if st.button('Delete'):
                            for i in Audio.each():
                                if i.val() == file_to_be_downloaded:
                                    db.child(user['localId']).child(
                                        'Audio_Files').child(i.key()).remove()
                                    st.experimental_rerun()

                    except TypeError:
                        st.info('No Files')

                elif pages == 'Neural Generator':

                    st.title('Neural Generator')
                    st.text(
                        'AI that generates music melodies with a variety og genres')
                    st.markdown("""
                                Find more information here""")

                    form = st.form(key='submit-form')
                    genre = form.selectbox(
                        'genre', options=['Classic', 'Gaming', 'Folk', 'Lofi'])
                    file_name = form.text_input(
                        'What would you like your file to be named?', placeholder='Name')
                    num_steps = form.slider(
                        'number of steps in 16th notes (Song length)', min_value=1, value=200, step=10, max_value=400)
                    predictability = form.number_input(
                        'predictibilty - the lower the number, the less preditable the generated output will be', min_value=0.1, max_value=1.0, step=0.1, value=0.8)
                    generate_button = form.form_submit_button('Generate')

                    if generate_button:
                        if not file_name:
                            st.error('Please enter a name')
                        else:
                            with st.spinner("Generating..."):

                                if genre == 'Classic':
                                    generate_beethoven(
                                        file_name=file_name, n_steps=num_steps, temperature=predictability)
                                elif genre == 'Gaming':
                                    generate_pokemon(
                                        file_name=file_name, n_steps=num_steps, temperature=predictability)
                                elif genre == 'Folk':
                                    generate_folk(
                                        file_name=file_name, n_steps=num_steps, temperature=predictability)
                                elif genre == 'Lofi':
                                    generate_lofi(
                                        file_name=file_name, n_steps=num_steps, temperature=predictability)

                                # match genre:
                                #     case "Classic":
                                #         generate_beethoven(file_name=file_name,n_steps=num_steps, temperature=predictability)
                                #     case "Gaming":
                                #         generate_pokemon(file_name=file_name,n_steps=num_steps, temperature=predictability)
                                #     case "Folk":
                                #         generate_folk(file_name=file_name,n_steps=num_steps, temperature=predictability)
                                #     case "Lofi":
                                #         generate_lofi(file_name=file_name,n_steps=num_steps, temperature=predictability)

                                midi_data = pretty_midi.PrettyMIDI(
                                    file_name+'.mid')
                                audio_data = midi_data.synthesize()
                                audio_data = np.int16(
                                    audio_data /
                                    np.max(np.abs(audio_data)) * 32767 * 0.9
                                )  # -- Normalize 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

                                audio_file = io.BytesIO()
                                wavfile.write(audio_file, 44100, audio_data)
                                st.audio(audio_file)

                                with open(file_name+'.mid', 'rb') as fp:
                                    btn = st.download_button(
                                        label='Download Midi File',
                                        data=fp,
                                        file_name=f'{file_name}.mid'

                                    )

            else:
                st.error('Invalid Email')
        else:
            st.error('Please fill email and password fields')
if choice == 'Home':
    
    with st.container():
        col1,col2,col3 = st.columns(3)
        with col1:
            st_lottie(load_lottie_file('https://assets2.lottiefiles.com/temp/lf20_ERpSsi.json'), key=1,height=200)
            
        with col2:
            #st.subheader('Neural Music Generator', anchor='center')
            st.markdown("<h1 style='text-align: center; color: gold;'>Neural Music Generator</h1>",
                        unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center; color: gold;'>A simple tool for creating music using AI</h4>",
                        unsafe_allow_html=True)
            
        with col3:
            st_lottie(load_lottie_file('https://assets2.lottiefiles.com/temp/lf20_ERpSsi.json'), height=200)



    with st.container():
        st.write('---')
        col1, col2 = st.columns(2)
        with col1:
            st.header("How It works")
            st.markdown(
                """
                <p1 style="font-size:23px;">
                This tool uses artificial neural networks to create AI generated music on the fly. The model has been trained using a variety of datasets in order to learn different genres and being able to create music based on the genre. Whether you 
                are an indepdent game developer, a complete begginer in music or a professional composers, Nueral Generator assists you in your creative endeavours. Create compelling melodies for your projects faster then ever before by leveraging the power 
                of AI-generated music </p1>  
                """, unsafe_allow_html=True)
        with col2:
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
                You will need to Sign up to the website to be able to use the neural generator. You can save your generated files in your profile so that you can use them later should you wish</p1> 
            
                <ol><b>
                    <li> Navgiate to the sign up page</li>
                    <li> Create an account with a valid email and password</li>
                    <li>Head to the login page and and login using your credenmtials</li>
                </ol>
                """, unsafe_allow_html=True)
            
        with col2:
            st.text('')
            st.text('')
            st.image('images/neural_gen.png')
            
    st.text('')    
    with st.container():
        st.write('---')
        st.header('Samples')
        st.write('Below are some of the samples created using the neural generator')
        
        
        st.text('Classical Music Samples')
        midi_to_wav('samples\classic_sample1.midi')
        midi_to_wav('samples\classic_sample2.midi')
        st.text('Lofi Sample')
        midi_to_wav('samples\lofi_sample1.midi')
        st.text('Game Music Sample')
        midi_to_wav('samples\game_sample1.midi')
        
