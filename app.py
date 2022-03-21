import requests
import webbrowser
import pyrebase
import streamlit as st
from streamlit_lottie import st_lottie, st_lottie_spinner
from models.pokemon_model.pokemon_model import generate_pokemon
from models.beethoven_model.beethoven_model import generate_beethoven
from models.folk_model.folk_model import generate_folk
from models.lofi_model.lofi_model import generate_lofi
import re
import numpy as np
import pretty_midi
import io
from scipy.io import wavfile
from streamlit_option_menu import option_menu
import time

# Page assets
st.set_page_config(page_title='Neural Melody Generator',
                   page_icon=':musical_note:', layout='wide',
                   initial_sidebar_state="collapsed")


def load_lottie_file(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_css(file):
    with open(file) as fp:
        st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)


lottie_file = load_lottie_file(
    "https://assets10.lottiefiles.com/packages/lf20_xnhvhcux.json")


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


# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()


customise_css = """
<style>
footer{
    visibility:hidden;
}
footer:after{
    content: 'Copyright @ 2022: Alireza M';
    display:block;
    position: relative;
    color:tomato;
}

</style>

"""


st.markdown("""
        <style>
            .css-18e3th9 {
                    padding-top: 1rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
            .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)


st.markdown(customise_css, unsafe_allow_html=True)

login_or_signup = st.sidebar.selectbox(
    options=['Login', 'Signup'], label='Account')

if login_or_signup == 'Signup':
    email = st.sidebar.text_input(
        'Please enter your email address', placeholder='Email')
    password = st.sidebar.text_input(
        'Please enter your password', type='password', placeholder='Password')
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    handle = st.sidebar.text_input(
        'Please input your app handle name', value='Default')
    submit = st.sidebar.button('Create my account')
    Login = st.sidebar.checkbox('Login/Logout', disabled=True)

    try:
        if submit:
            if email and password:
                if re.search(regex, email):
                    user = auth.create_user_with_email_and_password(
                        email, password)
                    st.sidebar.success('Your account is created successfully!')
                    st.balloons()

                    # Sign in
                    user = auth.sign_in_with_email_and_password(
                        email, password)

                    # creating a tree with the name localID with two child leafs that have values
                    db.child(user["localId"]).child("Handle").set(handle)
                    # givin the name of tree branch(localid) to the name
                    db.child(user["localId"]).child("ID").set(user["localId"])
                    # the ID is the same as the Auth UIID

                else:
                    st.sidebar.error('Invalid Email')
            else:
                st.sidebar.error('Please fill email and password fields')

    except requests.HTTPError as f:
        st.sidebar.error(
            'Error! Email is already registered or Password is too weak')

elif login_or_signup == 'Login':
    email = st.sidebar.text_input('Email', placeholder='JohnDoe@gmail.com')
    password = st.sidebar.text_input(
        'Password', type='password', placeholder='Password')
    Login = st.sidebar.checkbox('Login/Logout')
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if Login:
        if email and password:
            try:
                if re.search(regex, email):
                    user = auth.sign_in_with_email_and_password(
                        email, password)

                else:
                    st.sidebar.error('Please enter a valid email or password')
            except requests.HTTPError as f:
                if email:
                    st.sidebar.error('Email or Password incorreect')
                else:
                    st.sidebar.error('Email does not exist')
        else:
            st.sidebar.error('Please fill all the fields')


nav_bar = option_menu(None, ["Home", "How It Works", 'Neural Generator', "Account", "About"],
                      icons=['house', 'info-circle',
                             "music-note-beamed", "person-circle"],
                      menu_icon="cast", default_index=0, orientation="horizontal",
                      styles={
    "container": {"padding": "2!important", "background-color": "#fffff"},
    "icon": {"color": "orange", "font-size": "20px"},
    "nav-link": {"font-size": "20px", "text-align": "left", "margin": "5px", "--hover-color": "grey"},
    "nav-link-selected": {"background-color": ""},
}
)
if nav_bar == 'Neural Generator':
    st.title('Neural Generator')
    st.text(
        'Select your preference and get your free AI generated melody')
    st.markdown("""
                Find more information here""")

    form = st.form(key='submit-form')
    file_name = form.text_input('Select a unique name for your file', placeholder='Name',
                                help='The name must be unique to prevent the file from being overidden if you generate a file with the same name')
    genre = form.selectbox(
        'Genre', options=['Classic', 'Gaming', 'Folk', 'Lofi'])
    num_steps = form.slider('Number of steps to predict', min_value=1, value=200, step=10, max_value=400,
                            help='The number of musical steps you want the model the predict, the higher the number of steps, the longer the melody is going to be. You can think of this as the number of notes you want the model to predict from the start')
    key_sig = form.selectbox('Key Signature', options=[
                             'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'])
    predictability = form.number_input('Temperature - the lower the number, the less preditable the generated output will be', min_value=0.1, max_value=1.0, step=0.1, value=0.8,
                                       help='Temperature determines the rate at which the model picks the highest probabilstic output, i.e if the temperature is 0.8, theres a %80 chance that the model is going pick the the output with the highest probablity')
    generate_button = form.form_submit_button('Generate')

    if generate_button:
        if not file_name:
            st.error('Please enter a name')
        else:
            with st.spinner('Generating'):

                if genre == 'Classic':
                    generate_beethoven(
                        file_name=file_name, n_steps=num_steps, temperature=predictability, key_signature=key_sig)
                elif genre == 'Gaming':
                    generate_pokemon(
                        file_name=file_name, n_steps=num_steps, temperature=predictability, key_signature=key_sig)
                elif genre == 'Folk':
                    generate_folk(
                        file_name=file_name, n_steps=num_steps, temperature=predictability, key_signature=key_sig)
                elif genre == 'Lofi':
                    generate_lofi(
                        file_name=file_name, n_steps=num_steps, temperature=predictability, key_signature=key_sig)

                midi_data = pretty_midi.PrettyMIDI(
                    file_name+'.mid')
                audio_data = midi_data.synthesize()
                audio_data = np.int16(
                    audio_data /
                    np.max(np.abs(audio_data)) * 32767 * 0.9
                )   # -- Normalize 16 bit audio https://github.com/jkanner/streamlit-audio/blob/main/helper.py

                audio_file = io.BytesIO()
                wavfile.write(audio_file, 44100, audio_data)
                st.audio(audio_file)

                with open(file_name+'.mid', 'rb') as fp:
                    btn = st.download_button(
                        label='Download Midi File',
                        data=fp,
                        file_name=f'{file_name}.mid'

                    )

    if st.button('Save File'):

        if file_name:
            if Login:
                uid = user['localId']
                fireb_upload = storage.child(
                    uid+'_'+file_name+'.mid').put(file_name+'.mid', user['idToken'])
                stored_file = storage.child(
                    uid+'_'+file_name+'.mid').get_url(fireb_upload['downloadTokens'])
                db.child(uid).child('Audio_Files').push(stored_file)
                st.success('Done!')
                time.sleep(0.4)
                st.experimental_rerun()

            else:
                st.error('Please login to save your files')

        else:
            st.error('Please generate a file first')


elif nav_bar == 'Home':
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
                    <li>All done! You can now generate melodies</li>
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
        st.write('Below are some of the samples created using the neural generator')

        st.text('Classical Music Samples')
        midi_to_wav('samples/classic_sample1.midi')
        midi_to_wav('samples/classic_sample2.midi')
        st.text('Lofi Sample')
        midi_to_wav('samples/lofi_sample1.midi')
        st.text('Game Music Sample')
        midi_to_wav('samples/game_sample1.midi')

elif nav_bar == 'Account':
    # login_or_signup = st.selectbox(options=['Login', 'Signup'],label='')
    # if login_or_signup == 'Login':
    #         email = st.text_input(
    #         'Please enter your email address', placeholder='Email')
    #         password = st.text_input(
    #         'Please enter your password', type='password', placeholder='Password')
    #         login = st.checkbox('Login/Logout')
    #         regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if Login:
        # if Email and password:
        #     if re.search(regex, email):
        #         user = auth.sign_in_with_email_and_password(email, password)
        st.write(
            '<style>div.row-widget.stRadio > div{flex-direction:row;} ', unsafe_allow_html=True)

        # pages = st.radio(
        #     'Jump to', ['Neural Generator', 'Upload a file', 'Generated MIDIs'])

        # if pages == 'Upload a file':
        st.write('---')
        st.subheader('Upload A File')
        uploaded_file = st.file_uploader('Choose a file')
        upload = st.button('Upload')

        if upload:
            try:

                uid = user['localId']
                # fireb_upload = storage.child(uid).put(uploaded_file, user['idToken'])
                # stored_file = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                # db.child(uid).child('Audio_Files').push(stored_file)
                # st.success('File successfully uploaded')
                fireb_upload = storage.child(uid+'_'+uploaded_file.name).put(
                    uploaded_file, user['idToken'])
                stored_file = storage.child(uid+'_'+uploaded_file.name).get_url(
                    fireb_upload['downloadTokens'])
                db.child(uid).child(
                    'Audio_Files').push(stored_file)
                st.success('File successfully uploaded')

            except:
                st.error('Please select a file to upload!')

        Audio = db.child(user['localId']).child('Audio_Files').get()
        file_choices = []

        st.write('---')
        st.subheader('A list of all your uploaded files')

        try:
            for i in Audio.each():
                i_choice = i.val()
                file_choices.append(i_choice)
                st.write(i_choice)

            st.write('---')
            st.subheader('Delete A File')

            file_to_be_downloaded = st.selectbox(
                'Select the file you would like to Delete', file_choices)
            # if st.button('Download'):
            #     webbrowser.open(file_to_be_downloaded)
            if st.button('Delete'):
                for i in Audio.each():
                    if i.val() == file_to_be_downloaded:
                        db.child(user['localId']).child(
                            'Audio_Files').child(i.key()).remove()
                        st.experimental_rerun()

        except TypeError:
            st.info('No Files')

    else:
        st.warning('Please login to see account information')

elif nav_bar == 'How It Works':
    with st.container():
        st.write('---')
        col1, col2 = st.columns((1.2, 1))
        with col1:
            st.header("Artificial Neural Networks")
            st.markdown(
                """
                    <p1 style="font-size:20px;">
                    Neural Networks Form the base of deep learning, A subfield of machine learning where the alogrithms are inspired by the structure of the human brain. 
                    Neural networks take in data and train themselves to recoginise the patterns and predict the output for new sets of data.
                    </p1> 
                    </br>
                    </br>
                    </br>
                    <p1 style="font-size:20px;">
                    Neural Networks are made of layers of neurons. The neurons are the core processing units of the network. The first layer of the network is the input layer which recives the input data.
                    The output layer predicts our final output. In between, There are hidden layers which perform most of the computation. The ouput for each layer is passed as input for the next layer
                    until we reach the final layer. 
                    </p1>  
                    """, unsafe_allow_html=True)

        with col2:
            st.image('images/neural_nerworks.png')

    st.text('')
    st.write('---')

    with st.container():
        st.header("Types Of Neural Networks")
        st.markdown(
            """
            <p1 style="font-size:20px;">
            Technology is moving very fast specially in deep learning as new techniques and tools are developed everyday. while there are many types of neural networks, There are 3 common types;
            <b>Artificial Neural Networks(ANN)</b>, <b>Convolutional Neural Networks (CNN)</b> and <b>Recurrent Neural</b>. ANN is the classic neural network that was discussed. ANNs are versitile allround and used 
            in a variety of fields in deep learning. CNNs mainly prevellent image and video processing. CNNs have filters which extract the common features from images which are then used to 
            classify images. 
            </p1>  
            </br>
            </br>

            """, unsafe_allow_html=True)

        col1, col2 = st.columns((1, 2))
        with col1:
            st.image('images/nn_structure.png', width=550,
                     caption='A Basic Neural Networks Structure')
        with col2:
            st.image('images/cnn.jpeg', width=600,
                     caption='Convolutional Neural Network')

        st.write('')
        st.write('---')

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.header('Why Reucrrent Neural Networks?')

            st.markdown(
                """
                <p1 style="font-size:20px;">
                RNNs were created due to a few limitations in Feed Forward Neural networks:
                <ol>
                    <li>Feed-forward neural networks are not efficient enough to handle large amounts of sequential data</li>
                    <li>Feed-forward neural networks considers all datapoints independent therefore only consider the current input</li>
                    <li>Feed-forward neuralnetworks do not have a memory mechnism to deal with depedent datapoints like sequential data</li>
                </ol> 
                </p1>  
                """, unsafe_allow_html=True)

            st.text('')
            st.text('')
            st.text('')
            st.subheader('How Does Recurrent Neural Netowork Work? ')
            st.markdown(

                """
                <p1 style="font-size:20px;">
                Reccurent Neural Networks are desinged to deal with sequential data. This can be things such as weather forecast, text or musical notes where each datapoint dependent on its other datapoints.
                This is unlike CNNs and ANNs where datapoints are indepdent. RNNs are specially good for sequential data as they have sequential memory. RNNs have a looping  mechanism that acts a highway to allow information to flow
                from one step to the next which is called <b>hidden state </b>. This allows them to remmeber information about privious datapoints which subsequently determines the outcome for the next datapoint.
                </p1>
                """, unsafe_allow_html=True)

        with col2:
            for _ in range(17):
                st.text('')
            st.image('images/rnn_pics.gif', width=850,
                     caption='Working of Reucurrent Neural Network')

    st.write('---')

    with st.container():
        col1, col2 = st.columns(2)

        st.header("Music Generation Using Recurrent Neural Networks")
        st.markdown(
            """
            <p1 style="font-size:20px;">
            Melody consists of a sequence of notes and rests. Because of this , we can take a melody and transform it to a time series representation. <b>Time series</b> is a sequential data structure where we have samples 
            that are taken at equally spaced position in time.After the transformation, melody generation problem is now a time series prediction problem. Reuccrrent neural networks are the most effective way  
            time series prediction problems there we will use RNN to generate the next note given a melody.
            </p1>
            </br>
            </br> 
            <p1 style="font-size:20px;">
            Once the model is trained, we start with a seed melody. The seed melody is a set of beginning notes that we feed in to our trained network in order to predict the next note in melody. You can specify the number of steps
            you want the model to predict which ultimatly defines the length of your generated melody. 
            </p1> 

            """, unsafe_allow_html=True)
        st.text('')
        st.text('')
        col1, col2 = st.columns((1.2, 1))
        with col1:
            st.image('images/melody_rnn.png', width=800,
                     caption='we pass sets of songs and melodies to train our neural network. Network gradually learns to predict the next note when given a set of notes')
        with col2:
            st.image('images/predict.png', width=800, caption='The predicted note is then appended to the seed melody and then fed back in to the network to predict the next note. this process happens with same number of steps the user has specified')

        st.text('')


elif nav_bar == "About":
    with st.container():
        st.title("Hi, I am Alireza :wave:")
        st.header('A Computer Science Graduate from UK')
        st.markdown(
            """
            <p1 style="font-size:20px;">
             A Computer Science Graduate from UK
            </p1>
            </br>
            <p1 style="font-size:20px;">
            I am passionate about find ways to use python to create apps and websites for a more efficient and less time consuming data science experience
            </p1> 

            """, unsafe_allow_html=True)
        st.write("[My profile >](https://www.linkedin.com/in/alireza1999/)")

    with st.container():
        st.write('---')
        col1, col2 = st.columns((2, 1))

        with col1:
            st.header('What I do')
            st.write('###')
            st.markdown('<p style="font-size:20px;">I am currently a third year Computer Science student with a burning passion with python and machine learning </p>', unsafe_allow_html=True)

            st.markdown(

                """
                 <p style="font-size:20px;">
                On my freetime, I like to work create python web apps to:
                <ul>
                    <li>learn to leverage the power of Python in in web development</li>
                    <li>learn Data Analysis & Data Science to perform meaningful and impactful analyses</li>
                    <li>Leverage AI and machine learning to automate the boring stuff- "There is always an easier way"</li>
                </ul> 
                </p> 
                """, unsafe_allow_html=True)
            st.write("[My github >](https://github.com/AlirezaM1999)")
            st.write('#')
            st.markdown('<p style="font-size:20px;">You also find the source code for the app <a href="https://github.com/AlirezaM1999/streamlit_generate"> here</a></p>', unsafe_allow_html=True)

        with col2:
            st_lottie(load_lottie_file(
                'https://assets1.lottiefiles.com/packages/lf20_bp5lntrf.json'), width=550)

    with st.container():
        st.write('---')
        st.header('Get In Touch With Me')
        st.markdown(

                """
                <p1 style="font-size:20px;">
                If you have any inquiries or would like to get in touch with me, Fill the form below and I will get back to you as soon as possible
                </p1>
                """, unsafe_allow_html=True)
        st.write('#')
        
        
        
        contact = """
        <form action="https://formsubmit.co/ali.gabriel111@gmail.com" method="POST">
            <input type="text" name="name" placeholder="Name" required>
            <input type="email" name="email" placeholder="Email" required>
            <textarea name="message" placeholder="Message here" required></textarea>
            <button type="submit">Submit</button>
        </form>
        """
        col1, col2 = st.columns((2,1))
        with col1:
            st.markdown(contact, unsafe_allow_html=True)
            load_css(".style/style.css")
        

    with st.container():
        st.write('---')
        st.subheader('Copyright Disclaimer')
   
        st.markdown(

            """
                <p1 style="font-size:12px;">
               The Software product may include certain open source components that are subject to open source licenses (“Open Source Software”), in which case, the embedded Open Source Software is owned by a third party.
               The Open Source Software is not subject to the terms and conditions of this EULA. Instead, each item of Open Source Software is licensed under its applicable license terms which accompanies such Open Source Software.
               Nothing in this EULA limits your rights under, nor grants you rights that supersede, the terms and conditions of any applicable license terms for the Open Source Software. Any fees charged by GC in connection with the SOFTWARE, do not apply to the Open Source Software for which fees may not be charged under the applicable license terms.
               The terms and conditions of the applicable license for the Open Source Software are available on the LICENSE.txt file, which is provided with the SOFTWARE.
                </p1>
                """, unsafe_allow_html=True)
        
       
