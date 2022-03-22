import streamlit as st 
import requests, re 


def login_func(Login, email, password, regex, auth):
        
    if Login:
        if email and password:
            try:
                if re.search(regex, email):
                    user = auth.sign_in_with_email_and_password(
                        email, password)
                    
                    return user 

                else:
                    st.sidebar.error('Please enter a valid email or password')
            except requests.HTTPError as f:
                if email:
                    st.sidebar.error('Email or Password incorreect')
                else:
                    st.sidebar.error('Email does not exist')
        else:
            st.sidebar.error('Please fill all the fields')