
import streamlit as st 
from streamlit_lottie import st_lottie
from app import load_lottie_file
import requests


def load_lottie_file(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_css(file):
    with open(file) as fp:
        st.markdown(f"<style>{fp.read()}</style>", unsafe_allow_html=True)

def show_about_page():
    
    with st.container():
        st.title("Hi, I am Alireza :wave:")
        st.header('A Computer Science Graduate from UK')
        st.markdown(
            """
            <p1 style="font-size:20px;">
            </p1>
            <p1 style="font-size:20px;">
            I am passionate about finding ways to use python to create web apps and websites for a more efficient and less time consuming data science experience
            </p1> 

            """, unsafe_allow_html=True)
        st.write("[My profile >](https://www.linkedin.com/in/alireza1999/)")

    with st.container():
        st.write('---')
        col1, col2 = st.columns((2, 1))

        with col1:
            st.header('What I do')
            st.write('###')
            st.markdown('<p style="font-size:20px;">I am currently a third year Computer Science student with a burning passion for python and machine learning </p>', unsafe_allow_html=True)

            st.markdown(

                """
                <p style="font-size:20px;">
                On my free time, I like to create python web apps to:
                <ul>
                    <li>Learn to leverage the power of Python in web development</li>
                    <li>Learn data analysis & data science to perform meaningful and yield meaningful results</li>
                    <li>Leverage AI and machine learning to automate the boring stuff. There is always an easier way</li>
                </ul> 
                </p> 
                """, unsafe_allow_html=True)
            st.write("[My github >](https://github.com/AlirezaM1999)")
            st.write('#')
            st.markdown('<p style="font-size:20px;">You also find the source code for the app <a href="https://github.com/AlirezaM1999/streamlit_generate"> here</a></p>', unsafe_allow_html=True)

        with col2:
            st_lottie(load_lottie_file(
                'https://assets1.lottiefiles.com/packages/lf20_bp5lntrf.json'), width=497)

    with st.container():
        st.write('---')
        st.header('Get In Touch With Me')
        st.markdown(

                """
                <p1 style="font-size:20px;">
                If you have any inquiries or would like to get in touch with me, Complete the form below and I will get back to you as soon as possible
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