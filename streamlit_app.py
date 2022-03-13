from logging import exception
from types import NoneType
from urllib.error import HTTPError
import requests
import webbrowser
from numpy import datetime64
import pyrebase
import streamlit as st
from datetime import date, datetime
from fileinput import filename
import streamlit as st 
from models.pokemon_model.pokemon_model import generate_pokemon
from models.beethoven_model.beethoven_model import generate_beethoven
from models.folk_model.folk_model import generate_folk
from models.lofi_model.lofi_model import generate_lofi
import os 
import re


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



#Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

#Database 
db = firebase.database()
storage = firebase.storage()


st.sidebar.title("Neural Composer")


#Authentication 
choice = st.sidebar.selectbox('login/signup', ['Login', 'Sign up'])
email = st.sidebar.text_input('Please enter your email address', placeholder='Email')
password = st.sidebar.text_input('Please enter your password', type='password', placeholder='Password')
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

if choice == 'Sign up':
    handle = st.sidebar.text_input('Please input your app handle name', value='Default')
    submit = st.sidebar.button('Create my account')
    
    
    try:
        if submit:
            if email and password:
                if re.search(regex, email):
                    user = auth.create_user_with_email_and_password(email, password)
                    st.success('Your account is created successfully!')
                    st.balloons()
                    
                    #Sign in 
                    user = auth.sign_in_with_email_and_password(email, password)
                
                    #creating a tree with the name localID with two child leafs that have values
                    db.child(user["localId"]).child("Handle").set(handle)
                    db.child(user["localId"]).child("ID").set(user["localId"])  #givin the name of tree branch(localid) to the name
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
    login = st.sidebar.checkbox('Login/Logout')
    
    if login:
        if email and password:
            if re.search(regex, email):        
                user = auth.sign_in_with_email_and_password(email, password)
                st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                
                pages = st.radio('Jump to', ['Neural Generator','Upload a file', 'Generated MIDIs'])
                

                            
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
                            fireb_upload = storage.child(uploaded_file.name).put(uploaded_file, user['idToken'])
                            stored_file = storage.child(uploaded_file.name).get_url(fireb_upload['downloadTokens'])
                            db.child(uid).child('Audio_Files').push(stored_file)
                            st.success('File successfully uploaded')
                            
                        
                        except:
                            st.error('Please select a file to upload!')
                    
                elif pages == 'Generated MIDIs':
                    Audio  = db.child(user['localId']).child('Audio_Files').get()
                    file_choices = []
                    
                    try:
                        for i in Audio.each():
                            i_choice = i.val() 
                            file_choices.append(i_choice)
                            
                        file_to_be_downloaded = st.radio('Select the file you would like to download', file_choices)
                        if st.button('Download'):
                            webbrowser.open_new_tab(file_to_be_downloaded)
                        if st.button('Delete'):
                            for i in Audio.each():
                                if i.val() == file_to_be_downloaded:
                                    db.child(user['localId']).child('Audio_Files').child(i.key()).remove()
                                    st.experimental_rerun()
                            
                            
                    except TypeError:
                        st.info('No Files')
                            
                
                elif pages == 'Neural Generator':
                    
                    st.title('Neural Generator')
                    st.text('AI that generates music melodies with a variety og genres')
                    st.markdown("""
                                Find more information here""")



                    form = st.form(key='submit-form')
                    genre = form.selectbox('genre', options=['Classic', 'Gaming', 'Folk', 'Lofi'])
                    file_name = form.text_input('What would you like your file to be named?', placeholder='Name')
                    num_steps = form.slider('number of steps in 16th notes (Song length)',min_value=1, value=200, step=10, max_value=400)
                    predictability = form.number_input('predictibilty - the lower the number, the less preditable the generated output will be', min_value=0.1, max_value=1.0, step=0.1,value=0.8)
                    generate_button = form.form_submit_button('Generate')
                
                    



                    if generate_button:
                        if not file_name:
                            st.error('Please enter a name')
                        else:
                            with st.spinner("Generating..."):
                                
                                if genre == 'Classic':
                                    generate_beethoven(file_name=file_name,n_steps=num_steps, temperature=predictability)
                                elif  genre == 'Gaming':
                                    generate_pokemon(file_name=file_name,n_steps=num_steps, temperature=predictability)
                                elif  genre == 'Folk':
                                    generate_folk(file_name=file_name,n_steps=num_steps, temperature=predictability)
                                elif  genre == 'Lofi':
                                    generate_lofi(file_name=file_name,n_steps=num_steps, temperature=predictability)
                                
                                # match genre:
                                #     case "Classic":
                                #         generate_beethoven(file_name=file_name,n_steps=num_steps, temperature=predictability)         
                                #     case "Gaming":
                                #         generate_pokemon(file_name=file_name,n_steps=num_steps, temperature=predictability)
                                #     case "Folk":
                                #         generate_folk(file_name=file_name,n_steps=num_steps, temperature=predictability)
                                #     case "Lofi":
                                #         generate_lofi(file_name=file_name,n_steps=num_steps, temperature=predictability)
                                        
                                        
                                with open(file_name+'.mid', 'rb') as fp:
                                    btn = st.download_button(
                                        label='Download Midi File', 
                                        data = fp, 
                                        file_name=f'{file_name}.mid'
                                        
                                    )

            else:
                st.error('Invalid Email')
        else:
            st.error('Please fill email and password fields')                
