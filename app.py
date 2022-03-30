import pyrebase
import streamlit as st
from streamlit_option_menu import option_menu
from pages.home_page import *
from pages.HIW_page import *
from pages.neural_generator_page import generate_melody
from pages.account_page import show_account_page
from pages.about_page import *
from pages.log_in import login_func
from pages.sign_up import signup_func
import time


def configure_streamlit():
    # Page settings
    st.set_page_config(page_title='Neural Melody Generator',
                    page_icon=':musical_note:', layout='wide',
                    initial_sidebar_state="collapsed")
    
    
    #remove the default footer
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
    st.markdown(customise_css, unsafe_allow_html=True)
    #remove extra space from the top
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

def configure_database():
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
    
    return db, storage, auth



def main(db, storage, auth):
    user = None   
    login_or_signup = st.sidebar.selectbox(
        options=['Login', 'Signup'], label='Account')
    


    if login_or_signup == 'Signup':
        email = st.sidebar.text_input(
            'Please enter your email address', placeholder='Email')
        password = st.sidebar.text_input(
            'Please enter your password', type='password', placeholder='Password')
        regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        handle = st.sidebar.text_input(
            'Please input your app handle name', value='Default')
        submit = st.sidebar.button('Create my account')
        Login = st.sidebar.checkbox('Login/Logout', disabled=True)

        signup_func(auth, db, submit, email, password, regex,handle)

    elif login_or_signup == 'Login':
        email = st.sidebar.text_input('Email', placeholder='JohnDoe@gmail.com')
        password = st.sidebar.text_input(
        'Password', type='password', placeholder='Password')
        Login = st.sidebar.checkbox('Login/Logout')
        regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        
        user = login_func(Login, email, password, regex, auth)
        
        
        if not Login:
            with st.sidebar.expander('Forgot password?'):
                email = st.text_input('Enter your email', placeholder='JohnDoe@gmail.com')
                reset_pass = st.button('Submit')
                if reset_pass:
                    if email:
                        try:
                            auth.send_password_reset_email(email)
                            st.success('Reset link sent! Check your inbox')
                            
                        except:
                            st.error('Email not found!')
                    else:
                        st.error('Enter a valid email')
                    
            
        



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
        generate_melody(Login, user, storage, db)

    elif nav_bar == 'Home':
        home()

    elif nav_bar == 'Account':
        show_account_page(Login, storage, user, db)

    elif nav_bar == 'How It Works':
        hiw_page()

    elif nav_bar == "About":
        show_about_page()
   
   
   
            
if __name__ == "__main__":
    configure_streamlit()
    db, storage, auth = configure_database()
    main(db, storage, auth)
            
        

            
            
            
        
