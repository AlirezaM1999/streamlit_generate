import streamlit as st 
import requests, re 



def signup_func(auth, db, submit, email, password, regex,handle):
    try:
        if submit:
            if email and password:
                if re.search(regex, email):
                    
                    user = auth.create_user_with_email_and_password(email, password)
                    confirm_email = auth.send_email_verification(user['idToken'])
                    st.sidebar.success('Your account is created successfully!')
                    st.sidebar.success('Check your email')
                    st.balloons()

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